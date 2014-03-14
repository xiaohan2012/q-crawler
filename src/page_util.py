"""
page processing utility function
"""
import re, string

from pyquery import PyQuery as pq
from util import normalize_word

from nltk.corpus import stopwords
stopwords = stopwords.words ('english')

def clean (doc):
    """
    Cleaning the page:

    1. tags stripped
    2. irrelevant tag content removed (script, style...)
    """
    doc = pq (doc)
    
    doc.remove_namespaces ()#important for selecting elements
    
    doc ('script').remove ()
    doc ('style').remove ()

    return  doc.text ()


def html2words (html):
    """
    convert an html document to a list of words with some preprocessing:
    1, remove all punctuations
    2, remove all numbers

    To be implemented:
    . - / \ then can be used to separate words
    eg, os.path python/nltk python\gtk
    """
    text = clean (html)

    def split_text (text):
        return re.split("[%s\s]" %re.escape(string.punctuation), text)

    return '\t'.join(filter(lambda w: len (w) != 0 and w not in stopwords, #filter nonstop and noempty words
                            map(lambda w: normalize_word (w), split_text(text))))

if __name__ == "__main__":
    import sys, locale, codecs
    path = sys.argv [1]
    
    sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout);
    
    print html2words(open (path, 'r').read ())#no need to decode
