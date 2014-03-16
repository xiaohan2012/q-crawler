import setting
import unittest

from src.scraper import scrape_url_and_words, should_climbup, collect_words, should_collect_url, collect_urls

from pyquery import PyQuery as pq

class ScraperTest (unittest.TestCase):
    """
    test for the scraper for URL
    """
    def test_simple1 (self):
        """
        faked webpge
        """
        doc = open (setting.DIRNAME + '/pages/simple_page.html').read ()
        links = scrape_url_and_words (doc, "http://whut.edu.cn/cs/0809/random/random", level = 3)
        expected = [('http://whut.edu.cn/cs/0809/feng.html', 
                            sorted([("inside-tt1", -2), ("inside-tt2", -2), ("beside-tt1",-1),("beside-tt2",-1), ('presum', -1), ("text-inside-a", 0),("font-inside-a", 0),("inside-li-1", 1),("inside-li-2", 2), ("inside-em", 3)], 
                                   key=lambda (w,offset): offset))]
        self.assertEqual (expected, links)

    def test_simple_with_noisy_tags (self):
        """
        faked webpge with noisy tags such as script and style
        """
        doc = open (setting.DIRNAME + '/pages/simple_page_with_noise.html').read ()
        links = scrape_url_and_words (doc, "http://whut.edu.cn/cs/0809/random/random", level = 3)
        expected = [('http://whut.edu.cn/cs/0809/feng.html', 
                     sorted([("inside-tt1", -2), ("inside-tt2", -2), ("beside-tt1",-1),("beside-tt2",-1), ("text-inside-a", 0),("font-inside-a", 0),("inside-li-1", 1),("inside-li-2", 2), ("inside-em", 3)], 
                            key=lambda (w,offset): offset))]
        self.assertEqual (expected, 
                        links)
        
        
class ShouldCollect (unittest.TestCase):
    def test_should (self):
        self.assertTrue(should_collect_url ('http://en.wikipedia.org/wiki/Viterbi_algorithm', 
                                        'http://en.wikipedia.org/wiki/Baum%E2%80%93Welch_algorithm'))

    def test_shouldnot1 (self):
        self.assertFalse(should_collect_url ('http://en.wikipedia.org/wiki/Baum%E2%80%93Welch_algorithm#Forward_Procedure', 
                                             'http://en.wikipedia.org/wiki/Baum%E2%80%93Welch_algorithm'))
    def test_shouldnot2 (self):
        self.assertFalse(should_collect_url ('javascript:click ()', 
                                             'http://en.wikipedia.org/wiki/Baum%E2%80%93Welch_algorithm'))
                                             
        
class ShouldClimbupTest (unittest.TestCase):
    """
    test for the should_climbup function
    """
    def test_should_climbup1 (self):
        doc = pq(open (setting.DIRNAME + '/pages/scrape_testpage_1.html').read ())
        a = doc.find ('a')
        self.assertTrue(should_climbup (a))
        p = a.parent ()
        self.assertTrue(should_climbup (p))

    def test_should_climbup2 (self):
        doc = pq(open (setting.DIRNAME + '/pages/scrape_testpage_2.html').read ())
        a = doc.find ('a')
        self.assertTrue(should_climbup (a))
        p = a.parent ()
        self.assertFalse(should_climbup (p))

    def test_should_climbup3 (self):
        doc = pq(open (setting.DIRNAME + '/pages/simple_page.html').read ())
        a = doc.find ('a')
        self.assertTrue(should_climbup (a))
        li = a.parent ()
        self.assertFalse(should_climbup (li))

class CollectWordsTest (unittest.TestCase):
    """
    test for the collect_words function
    """
    def setUp (self):
        self.doc = pq(open (setting.DIRNAME + '/pages/simple_page.html').read ())
        
    def test_collect_words1 (self):
        prev_li = self.doc.find ('a').parent (). prev ()
        words = collect_words (prev_li, 1, 3)
        expected = [('beside-tt1', 1), ('beside-tt2', 1), ('inside-tt1', 2), ('inside-tt2', 2), ('presum', 1)]
        self.assertEqual (sorted (words), sorted (expected))

    def test_collect_words2 (self):
        next_li = self.doc.find ('a').parent().next ()
        words = collect_words (next_li, 1, 3)
        expected = [("inside-li-1", 1)]
        self.assertEqual (sorted (words), sorted (expected))

    def test_collect_words3 (self):
        """
        in vain
        """
        next_li = self.doc.find ('a').next ()
        words = collect_words (next_li, 1, 3)
        expected = []
        self.assertEqual (sorted (words), sorted (expected))

class ScrapeUrls (unittest.TestCase):
    def test_basic (self):
        html = open (setting.DIRNAME + '/pages/collect_url1.html').read ()
        urls = collect_urls (html, 'http://fakesite.com/subpage')
        self.assertEqual (urls, ['http://fakesite.com/feng.html'])
        
    
if __name__ == "__main__":
    unittest.main ()
