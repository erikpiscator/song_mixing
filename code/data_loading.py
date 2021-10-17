# Load data
import os
import numpy as np
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

    for root, dirs, files in os.walk(path, topdown=False):
        for file in files:
            

            audio_file = AudioSegment.from_wav(os.path.join(root, file))
            
            
            if audio_file.channels > 1:
                #make sure we are only using one channel. It may not matter.
                audio_file = audio_file.split_to_mono()[0]
            
            audio_array = np.array(audio_file.get_array_of_samples())
            song_name, artist_name = extract_names(file)
        
            song_dict = {
                "artist_name": artist_name,
                "song_name": song_name,
                "audio_segment": audio_file,
                "audio_array": audio_array,
                "song_path": path
            }
            
            playlist.append(song_dict)
        
    playlist = basic_feature_extraction(playlist)

    #playlist = load_bpm(playlist)

    return playlist


def extract_names(file):
    
    song_name,_,artist_name = file.partition(" - ")
    song_name = song_name[3:]

    artist_name,_,_ = artist_name.partition(".")
    
    return song_name, artist_name


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

    for song in playlist:
        
        song["frame_rate"] = song["audio_segment"].frame_rate
        
    return playlist


def load_bpm(playlist):

    #load csv with the bpms

    for song in playlist:
        # lookup the name on the csv and retrieve the actual bpms
        pass

    return playlist


def store_song(file, path):
    
    # pydub or whatever
    pass