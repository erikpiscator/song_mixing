
    # Iteratively:
    # Create the transition for one pair of songs
    #   - Time wrapping (progressivelly better)
    #   - Key changing (explore strategies)
    #   - Align all the sequence according to modified beats (try to do it with downbeats)
    #   - Volume fades to mix both

    
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
    previous_mix_cue_point, next_song_cue_point = select_cue_points(previous_mix, next_song)

    previous_mix, next_song = time_wrap(previous_mix, next_song, previous_mix_cue_point, next_song_cue_point)

    previous_mix, next_song = key_change(previous_mix, next_song, previous_mix_cue_point, next_song_cue_point)

    previous_mix, next_song = align(previous_mix, next_song, previous_mix_cue_point, next_song_cue_point)

    previous_mix, next_song = fade(previous_mix, next_song, previous_mix_cue_point, next_song_cue_point)

    mix = combine_songs(previous_mix, next_song)

    return mix

def select_cue_points(previous_mix, next_song):
    # several strategies

    #return previous_mix_cue_point, next_song_cue_point
    pass

    

def time_wrap(previous_mix, next_song, previous_mix_cue_point, next_song_cue_point):

    # rubberband

    # Wrap ALSO THE cue_points!!! (Both the normal ones and the selected ones)

    # Wrap ALSO THE beats!!!
    
    return previous_mix, next_song


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