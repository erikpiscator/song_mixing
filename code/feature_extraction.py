# Relevant feature extraction
    # Beat detection
    # Key detection
    # Structural segmentation

from madmom.features.beats import RNNBeatProcessor
from madmom.features.beats import DBNBeatTrackingProcessor

    
def feature_extraction(playlist):

    for song in playlist:

        beats_frames, bpm = beat_detection(song) 
        song['beat_times'] = beats_frames # Array like the samples marking with the beat ocurrs, ones/zeros
        song['estimated_bpm'] = bpm # Int

        key = key_detection(song)
        song['estimated_key'] = key # Probalby string or a int encoding of all the keys

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

def convert_to_frames(beat_times, song):

    beat_frames = (beat_times*song["frame_rate"]).astype(int)
    beat_frames_mapped = np.zeros_like(song["audio_array"])
    beat_frames_mapped[beat_frames] = 1
    
    return beat_frames_mapped