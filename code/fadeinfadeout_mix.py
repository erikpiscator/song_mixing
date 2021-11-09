import numpy as np
from data_loading import load_data, store_song
from transitions_creation import fade

def main():

    load_path = "../songs/dev_songs_house/"
    store_path = "../output/fadeinfadeout_mix_2.wav"

    # Load data
    playlist = load_data(load_path)

    mix = playlist[0]

    for i in range(1, len(playlist)):

        print(f"\tMixing tracks {i} and {i+1}...")

        previous_mix, next_song = fade(mix, playlist[i])
        mix = combine_songs(previous_mix, next_song)
    

    store_song(mix, store_path)


def combine_songs(previous_mix, next_song):

    mix = previous_mix.copy()

    previous_ending = len(previous_mix["audio_array"])-previous_mix["frame_rate"]*20

    next_audio_padded = np.pad(next_song["audio_array"], (previous_ending, 0), constant_values=0)

    mix["audio_array"] = next_audio_padded

    mix["audio_array"][: previous_mix["audio_array"].size] += previous_mix["audio_array"]

    return mix

if __name__ == "__main__":
    main()