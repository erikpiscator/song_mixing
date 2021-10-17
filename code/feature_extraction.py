# Relevant feature extraction
    # Beat detection
    # Key detection
    # Structural segmentation

from madmom.features.beats import RNNBeatProcessor
from madmom.features.beats import DBNBeatTrackingProcessor
from madmom.features.key import CNNKeyRecognitionProcessor
from madmom.features.key import key_prediction_to_label

    
def feature_extraction(playlist):

    for song in playlist:

        beats_frames, bpm = beat_detection(song) 
        song['beat_times'] = beats_frames # Array like the samples marking with the beat ocurrs, ones/zeros
        song['estimated_bpm'] = bpm # Int

        key_probabilities, key_label = key_detection(song)
        song['estimated_key'] = key_label # Probalby string or a int encoding of all the keys
        song['key_probabilities'] = key_probabilities

        cue_points = structural_segmentation(song)
        song['cue_points'] = cue_points # Array like the samples marking with the cue-point ocurrs

        # Maybe cut silences or if the cue-points in the beginning and the end are too extreme

    return playlist

# FEATURES

def beat_detection(song):
    
    proc = DBNBeatTrackingProcessor(fps=100)
    act = RNNBeatProcessor()(test_song["song_path"])
    beat_times = proc(act)

    # create the array of ones and zeros
    beat_frames = convert_to_frames(beat_times,song)

    # compute the bpm of the song
    # bpm = ?

    return beat_frames


def key_detection(song):

    #key = rubberband/madmom (experiment with both)
    
    proc = CNNKeyRecognitionProcessor()
    key_probabilities = proc(song["song_path"])
    key_label = key_prediction_to_label(key_probabilities)

    return key_probabilities, key_label


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

def convert_to_frames(beat_times, song):

    beat_frames = (beat_times*song["frame_rate"]).astype(int)
    beat_frames_mapped = np.zeros_like(song["audio_array"])
    beat_frames_mapped[beat_frames] = 1
    
    return beat_frames_mapped