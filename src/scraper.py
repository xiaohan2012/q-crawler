"""
The scraper that scrapes (text, surrounding text) from webpages
"""
import re, string, math
from itertools import chain
from pyquery import PyQuery as pq
from urlparse import urljoin

from url_validate import is_valid


def should_climbup (node):
    """
    determine if the node has some meaningful siblings (including text)
    stuff like "\n  " or "  \t   " is not meaningful
    """
    return len(filter(lambda c: c.strip () != "" if isinstance (c,basestring) else True, node.parent().contents())) == 1

def text2words (text):
    """
    from text to list of words
    
    """
    return map(lambda w: w.strip (), text. split ())
    
def collect_words (node, start_offset, max_offset):
    """
    collect (text, offset) pairs from node
    in which the offset is offseted by start_offset
    this process is done recursively within max_offset
    """
    if start_offset > max_offset: #stop when out of range
        return []


    real_contents = filter(lambda c: c.strip () != "" if isinstance (c,basestring) else True, 
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
    
def scrape_url (doc, page_url, level = 3):
    """
    Given the document, return the (url, surrounding words) pairs
    """
    doc = pq (doc)#to pq obj
    def get_words (linkelem):
        """
        Get the (word, offset) pairs representing the link
        """
        link = pq (linkelem)

        title = link.attr("title") != None and line2words(link.attr("title")) or ""
        anchor_text = link.text ()
        
        words = map(lambda w: (w, 0),#with offset 0
                    text2words (title) + text2words (anchor_text))
        
        starting_point = link
            
        #keep climbing to until the ancestor level has some siblings
        while should_climbup (starting_point):
            starting_point = starting_point.parent ()


        #creeping along the siblings, 
        #get each word and its offset to the link

        prevs, nexts = map(lambda elem: pq (elem),
                    starting_point.prevAll () [::-1]), map(lambda elem: pq (elem), 
                                                           starting_point.nextAll ())

        #creeping backward (the previous siblings)
        for offset, node in zip(xrange (1, level+1), prevs[: level]):
            to_be_negative_words = collect_words (node, offset, level)
            print to_be_negative_words
            words += map(lambda (_, offset): (_, -offset), to_be_negative_words)#reverse the offset (from positive integer to negative)
            
        #creeping forward (the next siblings)
        for offset, node in zip(xrange (1, level+1), nexts[: level]):
            words += collect_words (node, offset, level)
        
        return words
        
    link_word_pairs = map (lambda a: (urljoin (page_url, pq (a).attr ("href")), #from relative url path to absolute url path and collect the words
                                      sorted(get_words(a), key=lambda (w, offset): offset)),  #sort it according to offset
                           filter(lambda a: 
                                  pq (a).attr ("href") != None, #get urls that make sense
                                  doc.find ("a")))

    return link_word_pairs
