import numpy as np
from data_loading import load_data, store_song
from transitions_creation import fade

def main():

    load_path = "../songs/dev_songs_house/"
    store_path = "../listening_test/mixes/mix_A.wav"
    store_path_transition_times = "../listening_test/mixes/mix_A_transition_times.txt"

    # Load data
    playlist = load_data(load_path)

    with open(store_path_transition_times, "a") as myFile:
        myFile.write(f"\n-----Tracklist-----\n\n")
        for song in playlist:
            myFile.write(f"{song['song_name']} - {song['artist_name']}\n")
        myFile.write(f"\n-------------------\n\n")
        
    mix = playlist[0]

    for i in range(1, len(playlist)):

        print(f"\tMixing tracks {i} and {i+1}...")

        previous_mix, next_song = fade(mix, playlist[i])
        mix, transition_time = combine_songs(previous_mix, next_song)

        with open(store_path_transition_times, "a") as myFile:
            myFile.write(f"Transition {i} at time {convert(transition_time)}.\n")

    
        

    store_song(mix, store_path)


def combine_songs(previous_mix, next_song):

    mix = previous_mix.copy()

    previous_ending = len(previous_mix["audio_array"])-previous_mix["frame_rate"]*20

    next_audio_padded = np.pad(next_song["audio_array"], (previous_ending, 0), constant_values=0)

    mix["audio_array"] = next_audio_padded

    mix["audio_array"][: previous_mix["audio_array"].size] += previous_mix["audio_array"]

    return mix, np.round(previous_ending/previous_mix["frame_rate"],0)

def convert(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
      
    return "%02d:%02d" % (minutes, seconds)

if __name__ == "__main__":
    main()