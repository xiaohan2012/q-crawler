import setting
import unittest, nltk, random
from nltk.corpus import movie_reviews

from src.classifier import NBClassifier
from src.util import read_traindata

class NBClassifierToyTest (unittest.TestCase):
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

        expected = {u'spam': 0.8371836806110771, u'ham': 0.16281631938892294}

        for cls in expected.keys ():
            self.assertAlmostEqual (prediction [cls], expected [cls])

    def test_prediction2 (self):
        """
        test prediction for sample 2
        """
        sample = ['conference', 'registration', 'results', 'conference', 'online']
        prediction = self.classifier.predict (sample)

        expected =  {u'ham': 0.9683852022829362, u'spam': 0.031614797717063825}

        for cls in expected.keys ():
            self.assertAlmostEqual (prediction [cls], expected [cls])

    def test_unknown_words (self):
        """
        test prediction with unknown words
        """
        sample = ['conference', 'registration', 'results', 'conference', 'online', '(&^*^*&^*']
        prediction = self.classifier.predict (sample)
        
        expected = {u'ham': 0.9698452719061822, u'spam': 0.030154728093817886}

        for cls in expected.keys ():
            self.assertAlmostEqual (prediction [cls], expected [cls])

class NBClassifierRealTest (unittest.TestCase):
    """This time is real!"""

    def setUp (self):
        """
        first train the model
        """
        random.seed (123456)
        documents = [(map(lambda word: word.lower (), list(movie_reviews.words(fileid))), category)
                     for category in movie_reviews.categories()
                     for fileid in movie_reviews.fileids(category)]
        random.shuffle (documents)
        self.documents = documents
        
        self.classifier = NBClassifier ()
        self.classifier.train (documents)
        
    def est_prior (self):
        """
        first train the model
        """
        print self.classifier.cpd
        self.assertEqual(self.classifier.pt, {'pos': 0.5, 'neg': .5} )
        
if __name__ == "__main__":
    unittest.main ()
