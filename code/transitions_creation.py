
    # Iteratively:
    # Create the transition for one pair of songs
    #   - Time wrapping (progressivelly better)
    #   - Key changing (explore strategies)
    #   - Align all the sequence according to modified beats (try to do it with downbeats)
    #   - Volume fades to mix both
import numpy as np
import pyrubberband as pyrb
    
def create_transitions(queue):

    mix = queue[0]

    for i in range(1, len(queue)):

        mix = mix_pair(mix, queue[i])

    return mix



def mix_pair(previous_mix, next_song):
    '''
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
    '''

    # selecting the actual cue-points from all the posibilities
    previous_mix_cue_point = select_cue_points(previous_mix)

    previous_mix, next_song, ending_length, beginning_length = time_wrap(previous_mix, next_song, previous_mix_cue_point)

    previous_mix, next_song = key_change(previous_mix, next_song, previous_mix_cue_point, next_song_cue_point)

    previous_mix, next_song = align(previous_mix, next_song, previous_mix_cue_point, next_song_cue_point)

    previous_mix, next_song = fade(previous_mix, next_song, previous_mix_cue_point, next_song_cue_point)

    mix = combine_songs(previous_mix, next_song)

    return mix

def select_cue_points(previous_mix):

    cue_point = np.zeros_like(previous_mix['cue_points'])

    possible_idx = np.where(previous_mix['cue_points'] == 1)[0]
    
    cue_point_idx = possible_idx[possible_idx > previous_mix['cue_points'].size - 10*previous_mix['frame_rate']][0]    

    cue_point[cue_point_idx] = 1

    return cue_point

    

def time_wrap(previous_mix, next_song, previous_mix_cue_point):

    # rubberband

    # Wrap ALSO THE cue_points!!! (Both the normal ones and the selected ones)

    # Wrap ALSO THE beats!!!

    # simple approach: stretch to the avg freq

    avg_bpm = (previous_mix['estimated_bpm'] + next_song['estimated_bpm']) / 2

    cue_point_idx = np.where(previous_mix_cue_point == 1)[0][0]

    ending_length_samples = previous_mix['audio_array'].size - cue_point_idx
    ending_length_seconds = ending_length_samples / previous_mix['frame_rate']
    beginning_length_samples = int(ending_length_seconds * next_song['frame_rate'])

    ending_audio = previous_mix['audio_array'][-ending_length_samples:]
    ending_beats = previous_mix['beat_times'][-ending_length_samples:]
    ending_cue_points = previous_mix['cue_points'][-ending_length_samples:]
    ending_previous_cue_point = previous_mix_cue_point[-ending_length_samples:]

    beginning_audio = next_song['audio_array'][:beginning_length_samples]
    beginning_beats = next_song['beat_times'][:beginning_length_samples]
    beginning_cue_points = next_song['cue_points'][:beginning_length_samples]

    ending_stretching_ratio = avg_bpm/previous_mix['estimated_bpm']
    ending_audio_stretched = pyrb.time_stretch(ending_audio, previous_mix['frame_rate'], ending_stretching_ratio)
    ending_beats_stretched = pyrb.time_stretch(ending_beats, previous_mix['frame_rate'], ending_stretching_ratio)
    ending_cue_points_stretched = pyrb.time_stretch(ending_cue_points, previous_mix['frame_rate'], ending_stretching_ratio)
    ending_previous_cue_point_stretched = pyrb.time_stretch(ending_previous_cue_point, previous_mix['frame_rate'], ending_stretching_ratio)

    beginning_stretching_ratio = avg_bpm/next_song['estimated_bpm']
    beginning_audio_stretched = pyrb.time_stretch(beginning_audio, next_song['frame_rate'], beginning_stretching_ratio)
    beginning_beats_stretched = pyrb.time_stretch(beginning_beats, next_song['frame_rate'], beginning_stretching_ratio)
    beginning_cue_points_stretched = pyrb.time_stretch(beginning_cue_points, next_song['frame_rate'], beginning_stretching_ratio)

    new_previous = previous_mix.copy()
    new_previous['audio_array'] = np.concatenate((new_previous['audio_array'][:-ending_length_samples], ending_audio_stretched))
    new_previous['beat_times'] = np.concatenate((new_previous['audio_array'][:-ending_length_samples], ending_beats_stretched))
    new_previous['cue_points'] = np.concatenate((new_previous['cue_points'][:-ending_length_samples], ending_cue_points_stretched))

    new_next = next_song.copy()
    new_next['audio_array'] = np.concatenate((new_next['audio_array'][:-ending_length_samples], beginning_audio_stretched))
    new_next['beat_times'] = np.concatenate((new_next['audio_array'][:-ending_length_samples], beginning_beats_stretched))
    new_next['cue_points'] = np.concatenate((new_next['audio_array'][:-ending_length_samples], beginning_cue_points_stretched))
    

    
    return new_previous, new_next, ending_audio_stretched.size, beginning_audio_stretched.size


def key_change(previous_mix, next_song, previous_mix_cue_point, next_song_cue_point):

    # rubberband

    # Choose to change the key of next_song completely or only the transition part
    
    return previous_mix, next_song


def align(previous_mix, next_song, previous_mix_cue_point, next_song_cue_point):
    
    # just aligning the fist beat after previous_mix_cue_point with the first beat of next_song

    # previous_mix (array[len(previous_mix) + len(next_song) - alignment]) [:len(previous_mix)] = previous_mix values; [len(previous_mix):] = 0

    # next_song (array[len(previous_mix) + len(next_song) - alignment]) [:-len(next_song)] = 0; [-len(next_song):] = next_song values

    #return previous_mix, next_song

    pass


def fade(previous_mix, next_song, previous_mix_cue_point, next_song_cue_point):

    # explore fading libraries or strategies

    # fade previous_mix from previous_mix_cue_point on

    # fade next_song before next_song_cue_point

    #return previous_mix, next_song

    pass


def combine_songs(previous_mix, next_song):

    # sum all the arrays as needed

    #return mix

    pass