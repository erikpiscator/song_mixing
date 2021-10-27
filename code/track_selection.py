    # Choosing the first song
    # either:
    # iteratively choosing next song
    # tree search for optimal sequence


circle_of_fifths = {
	'major' : ['C','G','D','A' ,'E' ,'B' ,'F#','C#','G#','D#','A#', 'F'],
	'minor' : ['A','E','B','F#','C#','G#','D#','A#','F' ,'C' ,'G' ,'D']		
}
scale = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']

def get_song_sequence(playlist):

    not_in_queue = playlist.copy()

    not_in_queue.sort(key=lambda song: song['estimated_bpm'])

    queue = []
    
    queue.append(not_in_queue.pop(0))

    while not_in_queue:

        next_song = pick_next_song(queue[-1], not_in_queue)
        queue.append(next_song)
        not_in_queue.remove(next_song) 

    return queue


def pick_next_song(current, options):
    '''
        Explore several strategies

        Example:
            - Selecting candidate inside a +- bpm bounds
            - Picking the most similar one in key
            (see the paper for inspiration in distances between keys)
    '''
    
    threshold = 10

    selection = None
    #lower_bound, upper_bound = bpm_bounds(current["bpm"],thresh)
    current_bpm = current['estimated_bpm']
    current_key_distance = 12 # Maximum distance
    

    while not selection:

        for song in options:
            
            if song['estimated_bpm'] >= current_bpm - threshold and song['estimated_bpm'] <= current_bpm + threshold:
                
                optional_key_distance = key_distance_fifths(current['estimated_key'], current['estimated_mode'], song['estimated_key'], song['estimated_mode'])
                
                if optional_key_distance < current_key_distance:
                    
                    selection = song
                    current_key_distance = optional_key_distance
        
        threshold += 5
        

    return selection

# Do we need that?
def bpm_bounds(bpm,thresh):
    
    return bpm-thresh, bpm+thresh

def key_distance_semitones(key1, key2):

    idx1 = scale.index(key1)
    idx2 = scale.index(key2)

    diff = abs(idx1 - idx2)

    distance = min(diff, 12-diff)
    
    return distance

def key_distance_fifths(key1, mode1, key2, mode2):

    idx1 = circle_of_fifths[mode1].index(key1)
    idx2 = circle_of_fifths[mode2].index(key2)

    diff = abs(idx1 - idx2)

    distance = min(diff, 12-diff)
    
    return distance