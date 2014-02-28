import setting
import unittest

from src.url_validate import is_valid

class IsValidTest (unittest.TestCase):
    """
    Is valid url test
    """
    def test_basic (self):
        url = '/varieties/spam-classic-7-oz'
        self.assertFalse (is_valid (url))



if __name__ == "__main__":
    unittest.main ()
