# Relevant feature extraction
    # Beat detection
    # Key detection
    # Structural segmentation

import numpy as np
import scipy

from madmom.features.beats import RNNBeatProcessor
from madmom.features.beats import DBNBeatTrackingProcessor
from madmom.features.key import CNNKeyRecognitionProcessor
from madmom.features.key import key_prediction_to_label

import librosa

import matplotlib.pyplot as plt

    
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
    act = RNNBeatProcessor()(song["song_path"])
    beat_times = proc(act)

    # create the array of ones and zeros
    beat_frames = convert_to_frames(beat_times,song)

    # compute the bpm of the song
    bpm = beats_per_minute(beat_times,song)

    return beat_frames, bpm


def key_detection(song):

    #key = rubberband/madmom (experiment with both)
    
    proc = CNNKeyRecognitionProcessor()
    key_probabilities = proc(song["song_path"])
    key_label = key_prediction_to_label(key_probabilities)

    return key_probabilities, key_label


def structural_segmentation(song):
    
    ssm = structural_similarity_matrix(song)

    print('Shape')
    print(ssm.shape)

    print(ssm)

    fig, ax = plt.subplots()

    c = ax.pcolormesh(ssm, shading='auto', cmap='magma')
    ax.set_title("MFCC of first 10 seconds (Window size = 100ms)")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("MFCC Features")
    fig.colorbar(c, ax=ax, format='%+02.0f')

    plt.savefig('ssm.png')

    exit()

    cue_points = detect_cue_points(ssm)

    # create the array of ones and zeros

    pass


def structural_similarity_matrix(song):

    samples_per_beat = int(1.0/(song['estimated_bpm']/(60.0 * song['frame_rate'])))

    win_length = int(0.5 * samples_per_beat)
    hop_length = int(0.25 * samples_per_beat)

    print(win_length, hop_length)

    mspec = librosa.feature.melspectrogram(song['audio_array'], sr=song['frame_rate'], n_mels=128, n_fft=samples_per_beat, window="hann", hop_length=hop_length, win_length=win_length)

    print(mspec.shape)

    log_mspec = librosa.power_to_db(mspec, ref=np.max)

    mfcc = librosa.feature.mfcc(S = log_mspec, sr=song['frame_rate'], n_mfcc=13)

    print(mfcc.shape)

    length = mfcc.shape[1]

    print(length)

    ssm = np.zeros((length,length))

    for i in range(length):
        for j in range(length):
            ssm[i,j] = scipy.spatial.distance.cosine(mfcc[:,i], mfcc[:,j])

    return ssm


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

def beats_per_minute(beat_times, song):
    
    song_length = len(song["audio_array"])/song["frame_rate"]/60
    beats_count = len(beat_times)
    
    bpm = beats_count/song_length # We could have problems with the first and the last beat
    
    return bpm