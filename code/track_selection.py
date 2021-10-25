    # Choosing the first song
    # either:
    # iteratively choosing next song
    # tree search for optimal sequence


def get_song_sequence(playlist):

    unassigned = playlist.copy()

    queue = []

    # Both methods
    #if ___

    # choosing first song
    #queue.append(...)

    while unassigned:

        next_song = pick_next_song(queue[-1], unassigned)
        queue.append(next_song)
        unassigned.remove(next_song) 

    return queue

    # Tree search: TBI



def pick_next_song(current, options):
    '''
        Explore several strategies

        Example:
            - Selecting candidate inside a +- bpm bounds
            - Picking the most similar one in key
            (see the paper for inspiration in distances between keys)
    '''
    
    selection = options[0]
    lower_bound, upper_bound = bpm_bounds(current["bpm"],thresh)
    current_key_distance = key_distance(current["key"],selection["key"])
    

    for song in options:
        
        if song["bpm"] >= lower_bound && song["bpm"] <= upper_bound:
            
            optional_key_distance = key_distance(current["key"],song["key"])
            
            if optional_key_distance < current_key_distance:
                
                selection = song
        

    return selection

def bpm_bounds(bpm,thresh):
    
    return bpm-thresh, bpm+thresh

def key_distance(key1,key2):
    
    pass