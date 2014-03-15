"""
Utility function package
"""
import chardet, codecs

from classifier import NBClassifier

from nltk.stem.lancaster import LancasterStemmer
st = LancasterStemmer()

def read_traindata (filename):
    """
    Read the train dataset, given the filename
    """
    def split (l):
        """split one line into words and label"""
        segs = l.strip().split ('\t')
        label = segs [-1]
        words = segs [:-1]
        return words, label
    
    encoding = chardet.detect(open (filename).read ()) ['encoding']
    
    with codecs.open (filename, 'r', encoding) as f:
        for line in f.readlines ():
            row =  split (line)
            yield row

def normalize_word (word):
    """
    normalize a word in the sense that it is lowercase, stripped of newline or tabs and stemmed
    """
    return st.stem(word.strip ().lower ())

if __name__ == "__main__":
    data = read_traindata ('../data/pos')
    print list (data) [:10]
