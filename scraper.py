"""
The scraper that scrapes (text, surrounding text) from webpages
"""
from pyquery import PyQuery

def scrape_url (document):
    """
    Given the document, return the (url, surrounding text) pairs
    """
    
    #santize the document, remove all the tags except the <a> </a> tag
    
    #using the rule described in https://github.com/xiaohan2012/q-crawler#bag-of-words-of-the-url to get the surrouding text for each url

    #return them
