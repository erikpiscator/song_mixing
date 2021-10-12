
# Load data


def load_data(path):
    '''
    Output structure:
        list of dictionaries
            playlist[n] = {
                name (string)
                audio_array (np.array)
                sampling_rate (double)
                ...
                real_bpm (Int)
            }
    

    '''

    playlist = []

    # for os.walk()... :

        #song = AudioSegment.from_whatever(...)

        # extract song name

        #playlist.append(song)

    '''
    Output structure:
        list of dictionaries
            playlist[n] = {
                name (string)
                audio_segment (pydub.AudioSegment)
            }
    

    '''
        


    playlist = basic_feature_extraction(playlist)

    playlist = load_bpm(playlist)

    # return playlist

    pass


def basic_feature_extraction(playlist):
    '''
    Output structure:
        list of dictionaries
            playlist[n] = {
                name (string)
                audio_array (np.array)
                sampling_rate (double)
                ...
            }

    '''
    
    return playlist
    
    pass


def load_bpm(playlist):

    #load csv with the bpms

    for song in playlist:
        # lookup the name on the csv and retrieve the actual bpms
        pass

    return playlist


def store_song(file, path):
    
    # pydub or whatever
    
    pass