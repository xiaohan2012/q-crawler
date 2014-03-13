"""
page processing utility function
"""
import re, string

from pyquery import PyQuery as pq
from util import normalize_word

def clean (doc):
    """
    Cleaning the page:

    1. tags stripped
    2. irrelevant tag content removed (script, style...)
    """
    doc = pq (doc)
    doc ('script').remove ()
    doc ('style').remove ()

    return  doc.text ()

    
def html2words (string):
    """
    convert an html document to a list of words with some preprocessing:
    1, remove all punctuations
    2, remove all numbers
    """
    print 'cleaning'
    text = clean (string)

    print 'normalizing'
    return '\t'.join(map(lambda w: normalize_word (w), text.split ()))

if __name__ == "__main__":
    import sys, locale, codecs
    sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout);
    from codecs import open
    path = sys.argv [1]
    print html2words(open (path, 'r','utf8').read ())
