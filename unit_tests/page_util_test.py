import setting
import unittest

from src.page_util import clean, valid_word

class PageCleanTest (unittest.TestCase):
    """
    Test for page cleaning
    """
    def test_basic (self):
        doc = open (setting.DIRNAME + '/pages/page_util_simple1.html').read ()
        new_doc = clean (doc)
        #ensure script, style  are removed
        self.assertFalse ("script" in new_doc)
        self.assertFalse ("style" in new_doc)
        self.assertFalse ("script-snippet" in new_doc)

if __name__ == "__main__":
    unittest.main ()
