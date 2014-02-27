import setting
import unittest

from src.classifier import NBClassifier
from src.util import read_traindata

class NBClassifierTest (unittest.TestCase):
    def setUp (self):
        """
        first train the model
        """
        self.classifier = NBClassifier ()
        traindata = read_traindata (setting.DIRNAME + '/data/train.txt')
        self.classifier.train (traindata)

    def test_prediction1 (self):
        """
        test prediction for sample 1
        """
        sample = ['FREE', 'online', 'conference', '!!!']
        prediction = self.classifier.predict (sample)

        self.assertEqual (prediction, [(u'spam', 0.8371836806110771), (u'ham', 0.16281631938892294)])

    def test_prediction2 (self):
        """
        test prediction for sample 2
        """
        sample = ['conference', 'registration', 'results', 'conference', 'online']
        prediction = self.classifier.predict (sample)
        
        self.assertEqual (prediction, [(u'ham', 0.9683852022829362), (u'spam', 0.031614797717063825)])

    def test_unknown_words (self):
        """
        test prediction with unknown words
        """
        sample = ['conference', 'registration', 'results', 'conference', 'online', '(&^*^*&^*']
        prediction = self.classifier.predict (sample)
        
        self.assertEqual (prediction, [(u'ham', 0.9698452719061822), (u'spam', 0.030154728093817886)])


if __name__ == "__main__":
    unittest.main ()
