
# Load data
import os
import pydub
from pydub import AudioSegment

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

    for root, dirs, files in os.walk("./songs/house", topdown=False):
        for file in files:

            audio_file = AudioSegment.from_wav(os.path.join(root, file))

            name = extract_song_name(file)

            song_dict = {
                "song_name": name,
                "audio_segment": audio_file
            }
            playlist.append(song_dict)

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

def extract_song_name(file):
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

    frame_rate = audio_file.frame_rate
    
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