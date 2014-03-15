from classifier import NBClassifier
from util import read_traindata

import random
from pickle import load, dump

def performance_measure ():
    """
    """
    c = NBClassifier ()

    print 'reading data... '
    neg = list(read_traindata ('../data/neg'))
    pos = list(read_traindata ('../data/pos'))
    
    dataset = pos + neg
    random.shuffle(dataset)
    
    #partition training and testing set 4:1 
    train_set = dataset [:1500]
    test_set = dataset [1500:]
    
    print 'training...'
    c.train ( train_set )

    assert len(c.pt.keys ()) == 2
    assert len(c.cpd.keys ()) == 2
    assert 'pos' in c.cpd.keys ()
    assert 'neg' in c.cpd.keys ()

    print 'measuring performance'
    def get_label (doc):
        table = c.predict (doc)
        return max (table.keys (), key=lambda label: table[label])

    predicted_labels, true_labels = zip(*map(lambda (doc, label): (get_label (doc), label) , test_set))
    
    correct_count = sum(map (lambda (tl, pl): tl == pl and 1 or 0, zip (true_labels, predicted_labels)))
    print zip(predicted_labels, true_labels)
    print "Accuracy: %.5f" %(correct_count / float(len (true_labels)))

def train_classifier (path = '../data/classifier.pickle'):
    c = NBClassifier ()

    print 'reading data... '
    neg = list(read_traindata ('../data/neg'))
    pos = list(read_traindata ('../data/pos'))
    
    dataset = pos + neg

    print 'training...'
    c.train ( dataset )

    assert len(c.pt.keys ()) == 2
    assert len(c.cpd.keys ()) == 2

    
    dump(c, open('../data/classifier.pickle', 'w'))

def read_classifier (path):
    """
    read the pickled classifier
    """
    c = load (open (path, 'r'))
    
    #make sure things are correct
    assert len(c.pt.keys ()) == 2
    assert len(c.cpd.keys ()) == 2

    
    return c
    
if __name__ == "__main__":
    import sys
    action = sys.argv [1]
    if action == 'train':
        train_classifier ()
    elif action == 'measure':
        performance_measure ()
    else:
        print 'invalid option'
