# Relevant feature extraction
    # Beat detection
    # Key detection
    # Structural segmentation

from librosa.util.utils import frame
import numpy as np
import scipy
import sklearn

from madmom.features.beats import RNNBeatProcessor
from madmom.features.beats import DBNBeatTrackingProcessor
from madmom.features.key import CNNKeyRecognitionProcessor
from madmom.features.key import key_prediction_to_label

import librosa

from essentia.standard import FrameGenerator, PeakDetection

import utils

def feature_extraction(playlist):

    print('Extracting features')
    for i, song in enumerate(playlist):
        print(f'\tSong {i+1} / {len(playlist)}')

        print('\t\tEstimating beat...')
        beats_frames, bpm = beat_detection(song) 
        song['beat_times'] = beats_frames # Array like the samples marking with the beat ocurrs, ones/zeros
        song['estimated_bpm'] = bpm # Int

        print('\t\tEstimating key...')
        key_probabilities, key_label = key_detection(song)
        song['estimated_key'] = key_label.split(' ')[0] # Probalby string or a int encoding of all the keys
        song['estimated_mode'] = key_label.split(' ')[1]
        song['key_probabilities'] = key_probabilities

        print('\t\tEstimating cue-points')
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


def key_detection(song):

    #key = rubberband/madmom (experiment with both)
    
    proc = CNNKeyRecognitionProcessor()
    key_probabilities = proc(song["song_path"])
    key_label = key_prediction_to_label(key_probabilities)

    return key_probabilities, key_label


def structural_segmentation(song):

    kernel_dim = 32
    
    samples_per_beat = int(1.0/(song['estimated_bpm']/(60.0 * song['frame_rate'])))

    frame_size = int(0.5 * samples_per_beat)
    hop_size = int(0.25 * samples_per_beat)

    mfcc_ssm = mfcc_structural_similarity_matrix(song, frame_size=frame_size, hop_size=hop_size)
    rms_ssm = rms_structural_similarity_matrix(song, frame_size=frame_size, hop_size=hop_size)

    kernel = get_checkboard_kernel(kernel_dim)
    mfcc_novelty = apply_kernel(mfcc_ssm, kernel)
    rms_novelty = apply_kernel(rms_ssm, kernel)

    size_dif = mfcc_novelty.size - rms_novelty.size
    if size_dif > 0:
        rms_novelty = np.pad(rms_novelty, (0, np.abs(size_dif)), mode='edge')
    else:
        mfcc_novelty = np.pad(mfcc_novelty, (0, np.abs(size_dif)), mode='edge')

    novelty = mfcc_novelty * rms_novelty

    peaks_rel_pos, peaks_amp = detect_peaks(novelty)

    utils.save_cmap(mfcc_ssm, '../figures/mfcc_smm.png', ' MFCC Self-Similarity Matrix')
    utils.save_cmap(rms_ssm, '../figures/mfcc_smm.png', ' MFCC Self-Similarity Matrix')
    utils.save_cmap(kernel, '../figures/kernel', 'Checkboard Gaussian Kernel')
    utils.save_line(range(len(novelty)), novelty, '../figures/novelty.png', 'Novelty function', 'Frames', 'Amplitude')
    utils.save_line(peaks_rel_pos, peaks_amp, '../figures/peaks.png', 'Novelty peaks', 'Frames', 'Amplitude', '.')

    peaks_abs_pos = peaks_rel_pos * hop_size

    peak_times = np.zeros_like(song['audio_array'])

    for i in range(len(peaks_abs_pos)):
        beat_peak = find_near_beat(peaks_abs_pos[i], song['beat_times'])
        peak_times[beat_peak] = 1

    return peak_times



def mfcc_structural_similarity_matrix(song, frame_size, hop_size):

    mspec = librosa.feature.melspectrogram(song['audio_array'], sr=song['frame_rate'], n_mels=128, n_fft=frame_size, window="hann", win_length=frame_size, hop_length=hop_size,)

    log_mspec = librosa.power_to_db(mspec, ref=np.max)

    mfcc = librosa.feature.mfcc(S = log_mspec, sr=song['frame_rate'], n_mfcc=13)

    ssm = sklearn.metrics.pairwise.cosine_similarity(mfcc.T, mfcc.T)
    
    ssm -= np.average(ssm)
    m = np.min(ssm)
    M = np.max(ssm)
    ssm -= m
    ssm /= np.abs(m) + M

    return ssm


def rms_structural_similarity_matrix(song, frame_size, hop_size):

    rms_list = []
    for frame in FrameGenerator(song['audio_array'], frameSize = frame_size, hopSize = hop_size):
        rms_list.append(np.average(frame**2))

    ssm = sklearn.metrics.pairwise.pairwise_distances(np.array(rms_list).reshape(-1, 1))

    ssm -= np.average(ssm)
    m = np.min(ssm)
    M = np.max(ssm)
    ssm -= m
    ssm /= np.abs(m) + M

    return ssm


def get_checkboard_kernel(dim):

    gaussian_x = scipy.signal.gaussian(2*dim, std = dim/2.0).reshape((-1,1))
    gaussian_y = scipy.signal.gaussian(2*dim, std = dim/2.0).reshape((1,-1))

    kernel = np.dot(gaussian_x,gaussian_y)

    kernel[:dim,dim:] *= -1
    kernel[dim:,:dim] *= -1

    return kernel
    

def apply_kernel(ssm, kernel):

    kernel_dim = int(kernel.shape[0]/2)
    ssm_dim = ssm.shape[0]

    novelty = np.zeros(ssm_dim)

    ssm_padded = np.pad(ssm, kernel_dim, mode='edge')

    for index in range(ssm_dim):
        frame = ssm_padded[index:index+2*kernel_dim, index:index+2*kernel_dim]
        novelty[index] = np.sum(frame * kernel)
    
    novelty /= np.max(novelty)

    return novelty


def detect_peaks(novelty):

    threshold = np.max(novelty) * 0.05
    
    peakDetection = PeakDetection(interpolate=False, maxPeaks=100, orderBy='amplitude', range=len(novelty), maxPosition=len(novelty), threshold=threshold)
    peaks_pos, peaks_ampl = peakDetection(novelty.astype('single'))
    peaks_ampl = peaks_ampl[np.argsort(peaks_pos)]
    peaks_pos = peaks_pos[np.argsort(peaks_pos)]

    return peaks_pos, peaks_ampl


def find_near_beat(position, beat_times):

    position = int(position)

    i_low = 0
    i_up = 0
    while(position - i_low > 0 and beat_times[position-i_low] == 0):
        i_low += 1
    while(position + i_up < len(beat_times) and beat_times[position+i_up] == 0):
        i_up += 1

    if i_low < i_up:
        return position - i_low
    else:
        return position + i_up



def evaluate(playlist):

    for song in playlist:
        # Evaluating sort of acc in bpm detection
        pass

    # print or store or whatever
