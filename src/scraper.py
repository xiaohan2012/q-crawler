"""
The scraper that scrapes (text, surrounding text) from webpages
"""
import re, string, math
from itertools import chain
from pyquery import PyQuery as pq
from urlparse import urljoin

from util import normalize_word


def should_climbup (node):
    """
    determine if the node has some meaningful siblings (including text)
    stuff like "\n  " or "  \t   " is not meaningful
    """
    return len(filter(lambda c: c.strip () != "" if isinstance (c,basestring) else True, 
                      node.parent().contents())) == 1

def text2words (text):
    """
    from text to list of words (lowercase, stemmed, punctuation removed)
    
    """
    return map(lambda w: normalize_word (w), 
               text. split ())
    
def collect_words (node, start_offset, max_offset):
    """
    collect (text, offset) pairs from node
    in which the offset is offseted by start_offset
    this process is done recursively within max_offset
    """
    if start_offset > max_offset: #stop when out of range
        return []


    real_contents = filter(lambda c: c.strip () != "" if isinstance (c, basestring) else True, 
                           node.contents()) #filter out meaningless text
    
    is_text = lambda obj: isinstance (obj, basestring)
    
    text = filter(is_text, 
                  real_contents)
    
    words = [(word, start_offset) for t in text for word in text2words (t)]

    elems = filter(lambda obj: not is_text (obj), 
                   real_contents)

    for elem in elems:
        words += collect_words (pq (elem), start_offset + 1, max_offset)
    
    return words
    
def scrape_url_and_words (doc, page_url, level = 3, unnecessary_tags = ['script', 'style']):
    """
    Given the document, return the (url, surrounding words) pairs
    """
    doc = pq (doc)#to pq obj
    
    for tag in unnecessary_tags:#remove uncessary tags
        doc (tag).remove ()
        
    def get_words (linkelem):
        """
        Get the (word, offset) pairs representing the link
        """
        link = pq (linkelem)

        title = link.attr("title") != None and link.attr("title") or ""
        anchor_text = link.text ()
        
        words = map(lambda w: (w, 0),#with offset 0
                    text2words (title) + text2words (anchor_text))
        
        starting_point = link
        ancestor = link[0]
        #link.parent().parent()
        #keep climbing to until the ancestor level has some siblings
        #print "should go up", should_climbup (starting_point)
        while should_climbup (starting_point):
            starting_point = starting_point.parent ()
            ancestor = starting_point[0]

        siblings = filter(lambda c: c.strip () != "" if isinstance (c,basestring) else True, 
                          starting_point.parent ().contents ()) #remove those \n and \t stuff

        index = filter (lambda (idx, node): node == ancestor, 
                        enumerate (siblings)) [0] [0]  #find the position of the link

        #creeping along the siblings, 
        #get each word and its offset to the link
        prevs, nexts = map(lambda elem: pq (elem), siblings [:index] [::-1]), map(lambda elem: pq (elem),  siblings [index+1:])
        
        #creeping backward (the previous siblings)
        for offset, node in zip(xrange (1, level+1), prevs[: level]):
            to_be_negative_words = collect_words (node, offset, level)
            #print to_be_negative_words
            words += map(lambda (_, offset): (_, -offset), to_be_negative_words)#reverse the offset (from positive integer to negative)
            
        #creeping forward (the next siblings)
        for offset, node in zip(xrange (1, level+1), nexts[: level]):
            words += collect_words (node, offset, level)
        
        return words
        
    link_word_pairs = map (lambda a: (urljoin (page_url, pq (a).attr ("href")), #from relative url path to absolute url path and collect the words
                                      sorted(get_words(a), key=lambda (w, offset): offset)),  #sort it according to offset
                           filter(lambda a:
                                  pq (a).attr ("href") is not None and 
                                  should_collect_url (urljoin (page_url, pq (a).attr ("href")), 
                                                           page_url), #get urls that make sense
                                  doc.find ("a")))
    return link_word_pairs

def should_collect_url (url, page_url):
    """
    Determine whether the url should be collected based on the following criteria:
    
    - it does not point to `page_url`, an counter example: wikipedia.org/somepage#somefragment and wikipedia.org/somepage
    """
    from urlparse import urlparse
    url = urlparse (url)
    page_url = urlparse (page_url)
    if (url.netloc + url.path + url.params + url.query) != (page_url.netloc + page_url.path + page_url.params + page_url.query) and url.scheme in ("http", "https"):
        return True
    return False
    
def collect_urls (html, page_url):
    """
    collect subset of urls from the html 
    """
    return filter(lambda url: should_collect_url (url, page_url),
                  map(lambda a: urljoin(page_url, pq (a).attr ('href')), #get their hrefs
                      filter (lambda a: pq(a).attr ('href') is not None, #for those which have href attr
                              pq (html).find ('a'))))
    
if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        page_path = sys.argv[1]
        page_url = sys.argv[2]
        doc = open (page_path).read ()
        links = scrape_url (doc, page_url, level = 3)
        for url, words in links:
            print url, words
    else:
        print 'wrong number of arguments'
