"""
The scraper that scrapes (text, surrounding text) from webpages
"""
import re, string, math
from itertools import chain
from pyquery import PyQuery as pq

def strip_all_tags_except (doc, tag_names):
    """
    strip all tags in the doc except those included in `tag_names`

    return the 'sanitized' html string
    """
    def aux (contents):
        """
        auxiliary funciton:
        strip all the contents of tags except thos included in 'tag_names'
        """
        result = []
        for content in contents:
            if isinstance(content, str):
                result.append (content)
            elif content.tag in tag_names: #is string or the tag we want
                result.append (pq (content).outerHtml ())
            elif content is not None:
                result.extend(aux (pq(content).contents ()))

        return result
        
    return ' '.join(aux (pq(doc).contents ()))

def line2words (line):
    """
    remove redundent spaces and punctuations
    all words to lower case :-(

    then turn the line to words
    """
    return map(lambda w: w.lower (), re.sub ('[\t\n%s]+' %string.punctuation, ' ', line).split ())


def html2words (html):
    """
    convert one piece of html to words and tags
    """
    sequence = []
    #map the text to words
    for node in pq(html).contents ():

        if isinstance(node, str):
            sequence.extend (line2words (node))
        else:
            sequence.append (node)

    return sequence
    

def scrape_url (doc):
    """
    Given the document, return the (url, surrounding words) pairs
    """
    sufficient_word_number = 25
    
    striped_html = strip_all_tags_except (doc, ['a']) 
    sequence = html2words (striped_html) #the word, word, link, word... sequence
   
    def get_surrouding_words (linkelem):
        """
        The words representing the link
        
        The rule is:
        If the word count in title and link text > sufficient_word_number, then using the words in title and link text is ok
        Else, search from siblings(then parents) for more text. If there is no more text, forget about it
        """
        link = pq (linkelem)

        title = link.attr("title") != None and line2words(link.attr("title")) or []

        link_text = line2words(link.text())

        get_words = lambda seq: filter (lambda sth: isinstance (sth, str), seq)
        
        remaining_count = sufficient_word_number - len(title) - len (link_text)
 
        if remaining_count <= 0:
            return title + link_text
        else:
            
            index = sequence.index (linkelem)
            prepending_words = get_words (sequence [:index]); prepending_count = len(prepending_words)
            appending_words = get_words (sequence [index:]); appending_count = len(appending_words)
            
            prepending_half = int(math.floor(float(remaining_count) / 2))
            appending_half = int(math.ceil(float(remaining_count) / 2))
            if prepending_count + appending_count >= remaining_count:
                if appending_count <= appending_half: #prepending words are not enough to fill in half
                    return prepending_words [-(remaining_count - appending_count):] + title + link_text + appending_words
                elif prepending_count <= prepending_half: #appending words are not enough to fill in half
                    return prepending_words + title + link_text + appending_words [:(remaining_count - prepending_count)]
                else:#both are enough
                    return prepending_words [-prepending_half:] + title + link_text + appending_words [:appending_half]
            else: #that is it
                return prepending_words + title + link_text + appending_words
 
    links = map(lambda link: (pq(link).attr ('href'), get_surrouding_words (link)), filter(lambda ele: not isinstance(ele, str) and ele.tag == 'a', sequence))
    
    #return them
    return links
