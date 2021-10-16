# Relevant feature extraction
    # Beat detection
    # Key detection
    # Structural segmentation

from madmom.features.beats import RNNBeatProcessor
from madmom.features.beats import DBNBeatTrackingProcessor

    
def feature_extraction(playlist):

    for song in playlist:

        beats, bpm = beat_detection(song) 
        song['beat_times'] = beat_times # Array like the samples marking with the beat ocurrs
        song['estimated_bpm'] = bpm # Int

        key = key_detection(song)
        song['estimated_key'] = key # Probalby string or a int encoding of all the keys

        cue_points = structural_segmentation(song)
        song['cue_points'] = cue_points # Array like the samples marking with the cue-point ocurrs


        # Maybe cut silences or if the cue-points in the beginning and the end are too extreme

    return playlist

# FEATURES

def beat_detection(song):
    #NOTE: 'file' is suppose to be a .wav file (or similar).
    #It is not suppose to be an AudioSegment from pydub.
    #With this in mind, do we even need pydub?
    
    proc = DBNBeatTrackingProcessor(fps=100)
    act = RNNBeatProcessor()(test_song["song_path"])
    beat_times = proc(act)

    # create the array of ones and zeros

    # compute the bpm of the song

    #return beat_times, bpm

    pass


def key_detection(song):

    #key = rubberband/madmom (experiment with both)

    #return key

    pass


def structural_segmentation(song):
    
    ssm = structural_similarity_matrix(song)

    cue_points = detect_cue_points(ssm)

    # create the array of ones and zeros

    pass


def structural_similarity_matrix():
    pass


def detect_cue_points(ssm):
    pass


def evaluate(playlist):

    for song in playlist:
        # Evaluating sort of acc in bpm detection
        pass

    # print or store or whatever
