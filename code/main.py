# Hyperparams
# Peak selection threshold: 0.025
# Song selection BPM threshold: 4
# Transition length: 20s

from data_loading import load_data, store_song
from feature_extraction import feature_extraction, evaluate
from track_selection import get_song_sequence
from transitions_creation import create_transitions


def arg_parse():
    pass


def main():

    # Parse arguments
    arg_parse()
    load_path = "../songs/dev_songs_house/"
    store_path = "../songs/dev_songs_house_output/song_mix_new_14.wav"

    # Load data
    playlist = load_data(load_path)

    if not playlist:
        print("No song found")
        exit()

    # - Sequence of songs (in np array format) with minor features (e.g. Sampling rate)

    # Relevant feature extraction
    playlist = feature_extraction(playlist)

    # Compute evaluation stats and show/store
    # evaluate(playlist)

    # - Sequence of songs with their relevant features (dict)

    # Choosing the sequence
    queue = get_song_sequence(playlist)

    # - We will have the ordered sequence of songs

    # Create the transition for one pair of songs
    mix = create_transitions(queue)

    # - Long song mixed

    # Store the song in desired format
    store_song(mix, store_path)

def test_region():
    load_path = "../songs/test"
    playlist = load_data(load_path)

    print(playlist[0]["song_path"])

    feature_extraction(playlist)


if __name__ == "__main__":
    main()
