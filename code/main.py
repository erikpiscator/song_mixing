from data_loading import load_data, store_song
from feature_extraction import feature_extraction, evaluate
from track_selection import get_song_sequence
from transitions_creation import create_transitions


def arg_parse():
    pass


def main():

    # Parse arguments
    arg_parse()
    load_path = "./songs/house"
    store_path = "./song_mix.wav"

    # Load data

    playlist = load_data(load_path)
    
    # - Sequence of songs (in np array format) with minor features (e.g. Sampling rate)

    # Relevant feature extraction
    
    playlist = feature_extraction(playlist)

    # Compute evaluation stats and show/store

    evaluate(playlist)

    # - Sequence of songs with their relevant features (dict)

    # Choosing the sequence

    queue = get_song_sequence(playlist)

    # - We will have the ordered sequence of songs

    # Create the transition for one pair of songs

    mix = create_transitions(queue)

    # - Long song mixed

    # Store the song in desired format

    store_song(mix, store_path)



if __name__ == '__main__':
    main()
