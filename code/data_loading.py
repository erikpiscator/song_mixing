# Load data
import os
import numpy as np
from pydub import AudioSegment
import csv
import scipy

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

    print(f"Loading data from {path}...")

    playlist = []

    for root, dirs, files in os.walk(path, topdown=False):
        for file in files:
    
            audio_file = AudioSegment.from_wav(os.path.join(root, file))
            
            if audio_file.channels > 1:
                #make sure we are only using one channel. It may not matter.
                audio_file = audio_file.split_to_mono()[0]
            

            audio_array = np.array(audio_file.get_array_of_samples(), dtype=float)
            song_name, artist_name = extract_names(file)
        
            song_dict = {
                "artist_name": artist_name,
                "song_name": song_name,
                "audio_segment": audio_file,
                "audio_array": audio_array,
                "song_path": os.path.join(root, file)
            }

            
            
            playlist.append(song_dict)

    playlist = basic_feature_extraction(playlist)
    #playlist = load_true_bpm(playlist)

    print(f"\t{len(playlist)} songs loaded")

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


def load_true_bpm(playlist):

    #load csv with the bpms
    
    with open("songs.csv", "r") as file:
        csv_reader = csv.DictReader(file,delimiter=",")
        playlist_true_bpm = list(csv_reader)
    

    for song in playlist:
        flag = 0
        for song_ref in playlist_true_bpm:
            if song["song_name"] == song_ref["song_name"]:
                song["true_bpm"] = song_ref["bpm"]
                flag = 1
        if flag == 0:
            # Don't know if this is the best way of raising an error. 
            # Please change to a better one if you know one.
            print("No true bpm found for song:", song["song_name"])

    return playlist


def store_song(mix, path):
    
    scipy.io.wavfile.write(path, rate=mix["frame_rate"], data=mix["audio_array"].astype("int32"))