import setting
import unittest

from src.page_util import clean, html2words

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

    def test_real (self):
        doc = open (setting.DIRNAME + '/pages/with-style-tag.html').read ()
        new_doc = clean (doc)
        #ensure script, style  are removed
        self.assertFalse ("script" in new_doc)
        self.assertFalse (".borderless" in new_doc)
        self.assertFalse ("style" in new_doc)
        self.assertFalse ("script-snippet" in new_doc)

class Html2wordsTest (unittest.TestCase):
    """
    test for html2words
    """
    def test_basic (self):
        s = "a. b! c~ \n d \t "
        self.assertEqual (html2words (s), '\t'.join(['b','c','d']))
        
if __name__ == "__main__":
    unittest.main ()
