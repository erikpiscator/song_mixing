# Iteratively:
# Create the transition for one pair of songs
#   - Time wrapping (progressivelly better)
#   - Key changing (explore strategies)
#   - Align all the sequence according to modified beats (try to do it with downbeats)
#   - Volume fades to mix both
import numpy as np
import rubberband as rb


def create_transitions(queue):

    mix = queue[0]

    print("Creating_transitions...")

    for i in range(1, len(queue)):

        print(f"\tMixing tracks {i} and {i+1}...")
        mix = mix_pair(mix, queue[i])

    return mix


def mix_pair(previous_mix, next_song):
    """
    output
        mix = {
        name ([string])
        audio_array (np.array)
        sampling_rate ([double])
        ...
        real_bpm ([Int])
        estimated_bpm ([Int])
        estimated_key ([String])
        cue_points (np.array)
        }
    """

    # selecting the actual cue-points from all the posibilities
    previous_mix_cue_point = select_cue_points(previous_mix)

    print("\t\tAligning songs...")
    next_song_aligned = align(next_song)

    print("\t\tMixing beats...")
    (
        previous_mix_stretched,
        next_song_stretched,
        previous_ending,
        next_beginning,
    ) = time_wrap(previous_mix, next_song_aligned, previous_mix_cue_point)

    print("\t\tTransposing keys...")
    # previous_mix, next_song = key_change(previous_mix_stretched, next_song_stretched)

    print("\t\tFading transition...")
    previous_mix_faded, next_song_faded = fade(
        previous_mix_stretched, next_song_stretched, previous_ending, next_beginning
    )

    print("\t\tCombining tracks...")
    mix = combine_songs(previous_mix_faded, next_song_faded, previous_ending)

    return mix


def select_cue_points(previous_mix):

    max_transition_length = 20

    cue_point = np.zeros_like(previous_mix["cue_points"])

    possible_idx = np.where(previous_mix["cue_points"] == 1)[0]

    cue_point_idx = possible_idx[
        possible_idx
        > previous_mix["cue_points"].size
        - max_transition_length * previous_mix["frame_rate"]
    ][0]

    cue_point[cue_point_idx] = 1

    return cue_point


def align(next_song):

    first_beat = np.where(next_song["beat_times"] == 1)[0][0]

    new_next = next_song.copy()

    new_next["audio_array"] = next_song["audio_array"][first_beat:]
    new_next["beat_times"] = next_song["beat_times"][first_beat:]
    new_next["cue_points"] = next_song["cue_points"][first_beat:]

    return new_next


def time_wrap(previous_mix, next_song, previous_mix_cue_point):

    avg_bpm = (previous_mix["estimated_bpm"] + next_song["estimated_bpm"]) / 2

    ending_stretching_ratio = previous_mix["estimated_bpm"] / avg_bpm
    beginning_stretching_ratio = next_song["estimated_bpm"] / avg_bpm

    cue_point_idx = np.where(previous_mix_cue_point == 1)[0][0]

    ending_length_samples = previous_mix["audio_array"].size - cue_point_idx
    transition_length = ending_length_samples * ending_stretching_ratio
    transition_length_seconds = transition_length / previous_mix["frame_rate"]
    beginning_length_stretched = transition_length_seconds * next_song["frame_rate"]
    beginning_length_samples = int(
        beginning_length_stretched * beginning_stretching_ratio
    )

    ending_audio = previous_mix["audio_array"][-ending_length_samples:]
    ending_beats = previous_mix["beat_times"][-ending_length_samples:]
    beginning_audio = next_song["audio_array"][:beginning_length_samples]
    beginning_beats = next_song["beat_times"][:beginning_length_samples]

    ending_audio_stretched = rb.stretch(
        np.array(ending_audio, dtype="int32"),
        rate=previous_mix["frame_rate"],
        ratio=ending_stretching_ratio,
        crispness=5,
        formants=False,
        precise=True,
    )
    beginning_audio_stretched = rb.stretch(
        np.array(beginning_audio, dtype="int32"),
        rate=next_song["frame_rate"],
        ratio=beginning_stretching_ratio,
        crispness=5,
        formants=False,
        precise=True,
    )

    ending_beats_stretched = stretch_beats(
        ending_beats, ending_stretching_ratio, ending_audio_stretched.size
    )
    beginning_beats_stretched = stretch_beats(
        beginning_beats, beginning_stretching_ratio, beginning_audio_stretched.size
    )

    new_previous = previous_mix.copy()
    new_previous["audio_array"] = np.concatenate(
        (new_previous["audio_array"][:-ending_length_samples], ending_audio_stretched)
    )
    new_previous["beat_times"] = np.concatenate(
        (new_previous["beat_times"][:-ending_length_samples], ending_beats_stretched)
    )
    new_previous["cue_points"] = np.concatenate(
        (
            new_previous["cue_points"][:-ending_length_samples],
            np.zeros(
                ending_audio_stretched.size, dtype=previous_mix["cue_points"].dtype
            ),
        )
    )

    new_next = next_song.copy()
    new_next["audio_array"] = np.concatenate(
        (beginning_audio_stretched, new_next["audio_array"][beginning_length_samples:])
    )
    new_next["beat_times"] = np.concatenate(
        (beginning_beats_stretched, new_next["beat_times"][beginning_length_samples:])
    )
    new_next["cue_points"] = np.concatenate(
        (
            np.zeros(
                beginning_audio_stretched.size, dtype=next_song["cue_points"].dtype
            ),
            next_song["cue_points"][beginning_length_samples:],
        )
    )

    return (
        new_previous,
        new_next,
        new_previous["audio_array"][:-ending_length_samples].size,
        beginning_audio_stretched.size,
    )


def stretch_beats(beat_times, stretching_ratio, desired_length):

    new_beats = []

    zero_sequence_length = 0
    for i in beat_times:
        if i == 0:
            zero_sequence_length += 1
        elif i == 1:
            new_beats += [0] * int(zero_sequence_length * stretching_ratio)
            new_beats += [1]
            zero_sequence_length = 0

    diff = desired_length - len(new_beats)
    if diff > 0:
        new_beats += [0] * diff

    return np.array(new_beats, dtype=int)


def key_change(previous_mix, next_song, previous_mix_cue_point, next_song_cue_point):

    # rubberband

    # Choose to change the key of next_song completely or only the transition part

    return previous_mix, next_song


def fade(previous_mix, next_song, previous_mix_cue_point, next_song_cue_point):

    return previous_mix, next_song


def combine_songs(previous_mix, next_song, previous_ending):

    mix = previous_mix.copy()

    next_audio_padded = np.pad(
        next_song["audio_array"], (previous_ending, 0), constant_values=0
    )
    next_beat_padded = np.pad(
        next_song["beat_times"], (previous_ending, 0), constant_values=0
    )
    next_cue_padded = np.pad(
        next_song["cue_points"], (previous_ending, 0), constant_values=0
    )

    mix["audio_array"] = next_audio_padded
    mix["beat_times"] = next_beat_padded
    mix["cue_points"] = next_cue_padded

    mix["audio_array"][: previous_mix["audio_array"].size] += previous_mix[
        "audio_array"
    ]
    mix["beat_times"][: previous_mix["beat_times"].size] += previous_mix["beat_times"]
    mix["cue_points"][: previous_mix["cue_points"].size] += previous_mix["cue_points"]

    return mix
