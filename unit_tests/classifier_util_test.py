import setting
import unittest

from src.util import read_traindata
from src.classifier_util import read_classifier
from src.classifier import NBClassifier

class ReadClassifier (unittest.TestCase):
    """
    test reading the pickled classifier
    """
    def test_readable (self):
        path = 'data/classifier.pickle'
        
        # get the classifier
        classifier = NBClassifier ()
        traindata = read_traindata (setting.DIRNAME + '/data/train.txt')
        classifier.train (traindata)
        
        #save the classifier
        from pickle import dump
        dump(classifier, open(path, 'w'))

        #read the classifier
        same_classifier = read_classifier (path)

        #test
        self.assertEqual (same_classifier.cpd , classifier.cpd)
        self.assertEqual (same_classifier.pt , classifier.pt)
        self.assertEqual (same_classifier.label_freq () , classifier.label_freq ())
        self.assertEqual (same_classifier.feature_freq () , classifier.feature_freq ())
        self.assertEqual (same_classifier.vocabulary () , classifier.vocabulary ())
        self.assertEqual (same_classifier.labels (), classifier.labels ())
        
        
if __name__ == "__main__":
    unittest.main ()
