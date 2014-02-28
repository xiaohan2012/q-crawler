import setting
import unittest

from src.scraper import scrape_url, strip_all_tags_except, html2words

from pyquery import PyQuery as pq

class PreprocessingTest (unittest.TestCase):
    """
    test striping tags and html2words
    """
    def setUp (self):
        self.html = """
        <p>
          <span>
              Span 1 text
          </span>
          <span>
              Span 2 !!text
              <a href='http://feng'>link</a>
          </span>
          <div>
              Div text...
          </div>
          <span>
              Span 3.
              <a href='http://zhang'><sp>sometag</sp>zhanglink</a>
          </span>
        </p>
        """

    def test_basic (self):
        remaining = strip_all_tags_except (self.html, ['a'])
        expected = "Span 1 text Span 2 !!text <a href=\"http://feng\">link</a> Div text... Span 3. <a href=\"http://zhang\"><sp>sometag</sp>zhanglink</a>"

        actual = ' '.join(remaining.split ())
        
        self.assertEqual (actual, expected)

    def test_html2words (self):
        remaining = html2words(strip_all_tags_except (self.html, ['a']))

        expected = ["span", "1", "text", "span", "2", "text", "<a href=\"http://feng\">link</a>", "div", "text", "span", "3", "<a href=\"http://zhang\"><sp>sometag</sp>zhanglink</a>"]

        for sth,other in zip(remaining, expected):
            if isinstance(sth, str): #text
                self.assertEqual (sth, other)
            else:#html element
                self.assertEqual (pq(sth).outerHtml(), other)


                
class ScraperTest (unittest.TestCase):
    """
    test for the scraper for URL
    """
    def test_long_title (self):
        """
        title and link text exceeds 25
        """
        doc = open (setting.DIRNAME + '/pages/long_title_linktext.html').read ()
        links = scrape_url (doc)
        self.assertEqual ([('http://long_title.com', ['if', 'the', 'sentence', 'is', 'more', 'than', 'or', 'equal', 'to', '10', 'words', 'then', 'we', 'assume', 'only', 'this', 'sentence', 'is', 'about', 'the', 'url', 'it', 'is', 'really', 'really', 'long'])], links)

    def test_short_title (self):
        """
        title and link text exceeds 25
        """
        doc = open (setting.DIRNAME + '/pages/short_title.html').read ()
        links = scrape_url (doc)
        self.assertEqual ([('http://short_title.com', ['domain', 'bla', 'bla', 'bla', 'bla','bla', 'bla', 'bla', 'bla', 'bla', 'it', 'is', 'really', 'short', 'bla', 'bla', 'bla', 'bla', 'bla', 'bla', 'bla', 'bla', 'bla', 'bla', 'bla'])], links)

    def test_short_infront (self):
        """
        title and link words number fewer 25 thus need to get words from surrounding. In case the surrounding the text nodes
        """
        doc = open (setting.DIRNAME + '/pages/short_infront.html').read ()
        links = scrape_url (doc)
        
        self.assertEqual ([('http://short_title.com', ['example', 'domain', 'bla', 'bla', 'it', 'is', 'really', 'short', 'bla', 'bla', 'bla', 'bla', 'bla', 'bla', 'bla', 'bla', 'bla', 'bla', 'bla', 'bla', 'bla', 'bla', 'bla', 'bla', 'bla'])], links)

    def test_short_behind (self):
        """
        title and link words number fewer 25 thus need to get words from surrounding. In case the surrounding the element nodes
        """
        doc = open (setting.DIRNAME + '/pages/short_behind.html').read ()
        links = scrape_url (doc)
        self.assertEqual ([('http://short_title.com', ['bla', 'bla', 'bla', 'bla', 'bla', 'bla', 'bla', 'bla', 'bla',  'bla', 'bla', 'bla', 'bla', 'bla', 'bla', 'bla', 'bla', 'it', 'is', 'really', 'short', 'bla', 'bla', 'bla', 'bla'])], links)

    def test_insufficient_words (self):
        """
        title and link words number fewer 25 thus need to get words from surrounding. In case its ancestor
        """
        doc = open (setting.DIRNAME + '/pages/insufficient_words.html').read ()
        links = scrape_url (doc)
        self.assertEqual ([('http://short_title.com', ['insufficient', 'really', 'insufficient'])], links)
        
        
if __name__ == "__main__":
    unittest.main ()
