    # Relevant feature extraction
        # Beat detection
        # Key detection
        # Structural segmentation

def feature_extraction(playlist):

    for song in playlist:

        beats, bpm = beat_detection(song) 
        song['beats'] = beats # Array like the samples marking with the beat ocurrs
        song['estimated_bpm'] = bpm # Int

        key = key_detection(song)
        song['estimated_key'] = key # Probalby string or a int encoding of all the keys

        cue_points = structural_segmentation(song)
        song['cue_points'] = cue_points # Array like the samples marking with the cue-point ocurrs


        # Maybe cut silences or if the cue-points in the beginning and the end are too extreme

    return playlist

# FEATURES

def beat_detection(song):

    #beat_times = madmom

    # create the array of ones and zeros

    # compute the bpm of the song

    #return beat, bpm

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
