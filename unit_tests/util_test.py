import setting
import unittest

from src.util import read_traindata

class ReadTrainDataTest (unittest.TestCase):
    """
    test the read_traindata function
    """
    def setUp (self):
        self.filename = setting.DIRNAME + '/data/train.txt'
        print self.filename

    def test_ordinary (self):
        rows = list(read_traindata (self.filename))
        
        self.assertEqual(len(rows), 6)
        
        row0 = rows [0]
        self.assertEqual(row0 [0], ['FREE','online','!!!'])
        self.assertEqual(row0 [1], 'spam')
        

if __name__ == "__main__":
    unittest.main ()
