"""
Utility function package
"""
from codecs import open

def read_traindata (filename):
    """
    Read the train dataset, given the filename
    """
    def split (l):
        """split one line into words and label"""
        segs = l.strip().split (',')
        last_word, label = segs [-1].split (':') 
        words = segs [:len (segs)-1] + [last_word]
        return words, label
        
    with open (filename, 'r', 'utf8') as f:
        rows =  map (split,  f.readlines ())

    return rows
