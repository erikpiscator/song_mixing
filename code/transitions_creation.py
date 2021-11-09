# Iteratively:
# Create the transition for one pair of songs
#   - Time wrapping (progressivelly better)
#   - Key changing (explore strategies)
#   - Align all the sequence according to modified beats (try to do it with downbeats)
#   - Volume fades to mix both

import numpy as np
import rubberband as rb
from utils import convert

store_path_transition_times = "../listening_test/mixes/mix_B_info.txt"


def create_transitions(queue):

    mix = queue[0]

    print("Creating_transitions...")

    for i in range(1, len(queue)):

        print(f"\tMixing tracks {i} and {i+1}...")
        mix, transition_time = mix_pair(mix, queue[i])

        with open(store_path_transition_times, "a") as myFile:
            myFile.write(f"Transition {i} at time {convert(transition_time)}.\n")

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
    previous_mix_stretched,next_song_stretched,previous_ending,next_beginning = time_wrap(previous_mix, next_song_aligned, previous_mix_cue_point)

    #print("\t\tTransposing keys...")
    # previous_mix, next_song = key_change(previous_mix_stretched, next_song_stretched)

    print("\t\tFading transition...")
    previous_mix_faded, next_song_faded = fade(previous_mix_stretched, next_song_stretched)

    print("\t\tCombining tracks...")
    mix = combine_songs(previous_mix_faded, next_song_faded, previous_ending)

    return mix, previous_ending/previous_mix["frame_rate"]


def select_cue_points(previous_mix):

    cue_point = np.zeros_like(previous_mix["cue_points"])
    possible_idx = np.where(previous_mix["cue_points"] == 1)[0]

    flag = False
    i = 1
    while flag == False:
        # select first cue point that are at least 20s from end.
        if (len(previous_mix["audio_array"]) - possible_idx[-i]) / previous_mix["frame_rate"] >= 20:
            cue_point[possible_idx[-i]] = 1
            flag = True
        i += 1
    
    return cue_point


def align(next_song):

    first_beat = np.where(next_song["beat_times"] == 1)[0][0]

    new_next = next_song.copy()

    new_next["audio_array"] = next_song["audio_array"][first_beat:]
    new_next["beat_times"] = next_song["beat_times"][first_beat:]
    new_next["cue_points"] = next_song["cue_points"][first_beat:]

    return new_next


def time_wrap(previous_mix, next_song, previous_mix_cue_point):

    transition_length_seconds = 20
    avg_bpm = (previous_mix["estimated_bpm"] + next_song["estimated_bpm"]) / 2

    ending_stretching_ratio = previous_mix["estimated_bpm"] / avg_bpm
    beginning_stretching_ratio = next_song["estimated_bpm"] / avg_bpm

    cue_point_idx = np.where(previous_mix_cue_point == 1)[0][0]

    transition_length_prev_frames_stretched = transition_length_seconds * previous_mix["frame_rate"]
    transition_length_prev_frames = int(transition_length_prev_frames_stretched / ending_stretching_ratio)

    transition_length_next_frames_stretched = transition_length_seconds * next_song["frame_rate"]
    transition_length_next_frames = int(transition_length_next_frames_stretched / beginning_stretching_ratio)

    ending_audio = previous_mix["audio_array"][cue_point_idx : cue_point_idx + transition_length_prev_frames]
    ending_beats = previous_mix["beat_times"][cue_point_idx : cue_point_idx + transition_length_prev_frames]
    beginning_audio = next_song["audio_array"][:transition_length_next_frames]
    beginning_beats = next_song["beat_times"][:transition_length_next_frames]


    ending_audio_stretched = rb.stretch(np.array(ending_audio, dtype="int32"),rate=previous_mix["frame_rate"],ratio=ending_stretching_ratio,crispness=6,formants=False,precise=True)
    beginning_audio_stretched = rb.stretch(np.array(beginning_audio, dtype="int32"),rate=next_song["frame_rate"],ratio=beginning_stretching_ratio,crispness=6,formants=False,precise=True)

    ending_beats_stretched = stretch_beats(ending_beats, ending_stretching_ratio, ending_audio_stretched.size)
    beginning_beats_stretched = stretch_beats(beginning_beats, beginning_stretching_ratio, beginning_audio_stretched.size)

    previous_mix["estimated_bpm"] = next_song["estimated_bpm"]

    new_previous = previous_mix.copy()
    
    new_previous["audio_array"] = np.concatenate((new_previous["audio_array"][:cue_point_idx], ending_audio_stretched))
    new_previous["beat_times"] = np.concatenate((new_previous["beat_times"][:cue_point_idx], ending_beats_stretched))
    new_previous["cue_points"] = np.concatenate((new_previous["cue_points"][:cue_point_idx],np.zeros(ending_audio_stretched.size, dtype=previous_mix["cue_points"].dtype)))

    new_next = next_song.copy()
    new_next["audio_array"] = np.concatenate((beginning_audio_stretched, new_next["audio_array"][transition_length_next_frames:]))
    new_next["beat_times"] = np.concatenate((beginning_beats_stretched, new_next["beat_times"][transition_length_next_frames:]))
    new_next["cue_points"] = np.concatenate((np.zeros(beginning_audio_stretched.size, dtype=next_song["cue_points"].dtype),next_song["cue_points"][transition_length_next_frames:]))

    return (new_previous,new_next,new_previous["audio_array"][:cue_point_idx].size,beginning_audio_stretched.size)

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


def fade(previous_mix, next_song):

    fade_seconds = 20
    fade_frames = fade_seconds * previous_mix["frame_rate"]

    for i in range(fade_frames):

        #exponential fade
        #previous_mix["audio_array"][-i] = previous_mix["audio_array"][-i] * (1.1 - np.exp(2.398 * (1 - i / fade_frames)) * 0.1)
        #next_song["audio_array"][i] = next_song["audio_array"][i] * (0.1 * np.exp(2.398 * i / fade_frames) - 0.1)

        #linear fade
        previous_mix["audio_array"][-i] = previous_mix["audio_array"][-i] * i/fade_frames
        next_song["audio_array"][i] = next_song["audio_array"][i] * i/fade_frames

    return previous_mix, next_song


def combine_songs(previous_mix, next_song, previous_ending):

    mix = previous_mix.copy()

    next_audio_padded = np.pad(next_song["audio_array"], (previous_ending, 0), constant_values=0)
    next_beat_padded = np.pad(next_song["beat_times"], (previous_ending, 0), constant_values=0)
    next_cue_padded = np.pad(next_song["cue_points"], (previous_ending, 0), constant_values=0)

    mix["audio_array"] = next_audio_padded
    mix["beat_times"] = next_beat_padded
    mix["cue_points"] = next_cue_padded

    mix["audio_array"][: previous_mix["audio_array"].size] += previous_mix["audio_array"]
    mix["beat_times"][: previous_mix["beat_times"].size] += previous_mix["beat_times"]
    mix["cue_points"][: previous_mix["cue_points"].size] += previous_mix["cue_points"]

    return mix
