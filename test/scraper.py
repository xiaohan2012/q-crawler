import setting
import unittest

from src.scraper import scrape_url, recursive_contents

from pyquery import PyQuery as pq

class RecursiveContentsTest (unittest.TestCase):
    
    
    def test_basic (self):
        
        html = """
        <p>
          <span>
              Span 1 text
          </span>
          <span>
              Span 2 text
              <a href='http://feng'>link</a>
          </span>
          <div>
              Div text
          </div>
          <span>
              Span 1
          </span>
        </p>
        """.replace ('\n', '')
        
        
        node = pq (html)

        contents = recursive_contents (node)

        # check the tags
        tags = map(lambda node: node.tag, filter(lambda n: not isinstance(n, str), contents)) #get all the tags
        
        self.assertEqual(tags, ['span', 'a', 'div', 'span'])

        # check the text 
        text = map(lambda node: str (node).strip (), filter(lambda n: isinstance(n, str) and len(n.strip ()) > 0, contents)) #non whitespace text
        self.assertEqual(text, ['Span 2 text'])

    def test_basic1 (self):
        html = """
<div>
    <p>
      insufficient
      <a href="http://short_title.com" title="" >really insuffient</a>
    </p>
</div>
        """
        node = pq (html)

        contents = recursive_contents (node)

        # check the tags
        tags = map(lambda node: node.tag, filter(lambda n: not isinstance(n, str), contents)) #get all the tags
        
        self.assertEqual(tags, ['a'])

        # check the text 
        text = map(lambda node: str (node).strip (), filter(lambda n: isinstance(n, str) and len(n.strip ()) > 0, contents)) #non whitespace text
        self.assertEqual(text, ['insufficient'])
        
class ScraperTest (unittest.TestCase):
    """
    test for the scraper for URL
    """
    def test_long_title_linktext (self):
        """
        title and link text exceeds 25
        """
        doc = open ('pages/long_title_linktext.html').read ()
        links = scrape_url (doc)
        self.assertEqual ([('http://long_title.com', ['if', 'the', 'sentence', 'is', 'more', 'than', 'or', 'equal', 'to', '10', 'words', 'then', 'we', 'assume', 'only', 'this', 'sentence', 'is', 'about', 'the', 'url', 'it', 'is', 'really', 'really', 'long'])], links)

    def test_short_title_linktext_with_text_node (self):
        """
        title and link words number fewer 25 thus need to get words from surrounding. In case the surrounding the text nodes
        """
        doc = open ('pages/short_title_linktext.html').read ()
        links = scrape_url (doc)
        self.assertEqual ([('http://short_title.com', ['bla', 'bla', 'bla', 'bla', 'bla', 'bla', 'bla', 'bla', 'bla', 'it', 'is', 'really', 'short', 'bla', 'bla', 'bla', 'bla', 'bla', 'bla', 'bla', 'bla', 'bla', 'bla', 'bla', 'bla'])], links)

    def test_short_title_linktext_with_siblings (self):
        """
        title and link words number fewer 25 thus need to get words from surrounding. In case the surrounding the element nodes
        """
        doc = open ('pages/short_title_linktext_using_span.html').read ()
        links = scrape_url (doc)
        self.assertEqual ([('http://short_title.com', ['bla', 'bla', 'bla', 'bla', 'bla', 'bla', 'bla', 'bla', 'bla', 'it', 'is', 'really', 'short', 'bla', 'bla', 'bla', 'bla', 'bla', 'bla', 'bla', 'bla', 'bla', 'bla', 'bla', 'bla'])], links)

    def test_short_title_linktext_using_ancestor (self):
        """
        title and link words number fewer 25 thus need to get words from surrounding. In case its ancestor
        """
        doc = open ('pages/short_title_linktext_using_ancestor.html').read ()
        links = scrape_url (doc)
        self.assertEqual ([('http://short_title.com', ['bla', 'bla', 'bla', 'bla', 'bla', 'bla', 'bla', 'bla', 'bla', 'it', 'is', 'really', 'short', 'bla', 'bla', 'bla', 'bla', 'bla', 'bla', 'bla', 'bla', 'bla', 'bla', 'bla', 'bla'])], links)

    def test_insufficient_words (self):
        """
        title and link words number fewer 25 thus need to get words from surrounding. In case its ancestor
        """
        doc = open ('pages/insufficient_words.html').read ()
        links = scrape_url (doc)
        self.assertEqual ([('http://short_title.com', ['insufficient', 'really', 'insufficient'])], links)
        
        
if __name__ == "__main__":
    unittest.main ()
