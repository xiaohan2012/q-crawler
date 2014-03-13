"""
Utility function package
"""
from codecs import open

from nltk.stem.lancaster import LancasterStemmer
st = LancasterStemmer()

def read_traindata (filename):
    """
    Read the train dataset, given the filename
    """
    def split (l):
        """split one line into words and label"""
        segs = l.strip().split ('\t')
        last_word, label = segs [-1].split (':') 
        words = segs [:len (segs)-1] + [last_word]
        return words, label
        
    with open (filename, 'r', 'utf8') as f:
        rows =  map (split,  f.readlines ())

    return rows

def normalize_word (word):
    """
    normalize a word in the sense that it is lowercase, stripped of newline or tabs and stemmed
    """
    return st.stem(word.strip ().lower ())
