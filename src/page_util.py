"""
page processing utility function
"""
from pyquery import PyQuery as pq

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
