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

       nex_song = pick_next_song(queue[-1], unassigned)
       queue.append(nex_song)
       unassigned.remove(nex_song) 

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

    for song in options:

        #if song is better option than selection, pick song

        pass

    #return selection  


    pass