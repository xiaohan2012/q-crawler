"""
The scraper that scrapes (text, surrounding text) from webpages
"""
import re, string
from itertools import chain
from pyquery import PyQuery

def recursive_contents (node):
    """
    recursively get the contents of a node
    
    Example: 
    p
     span
     span
         #some-text
         a
     div
        span
    should return something like:
    [p span #some-text a div span]

    """
    contents = []
    node = PyQuery(node)
    if len(node.children ()) == 0: #no children
        return [node [0]]
    else: #has children
        for n in node.contents ():
            if isinstance(n, str):
                contents.append (n)
            else:
                contents.extend (recursive_contents (n))
    return contents
    
def scrape_url (doc):
    """
    Given the document, return the (url, surrounding words) pairs
    """
    sufficient_word_number = 25
    def line2words (line):
        """
        remove redundent spaces and punctuations
        all words to lower case :-(

        then turn the line to words
        """
        return map(lambda w: w.lower (), re.sub ('[\t\n%s]+' %string.punctuation, ' ', line).split ())

    def get_link_words (link):
        """
        The words representing the link
        
        The rule is:
        If the word count in title and link text > sufficient_word_number, then using the words in title and link text is ok
        Else, search from siblings(then parents) for more text. If there is no more text, forget about it
        """
        link = PyQuery (link)

        title = line2words(link.attr("title"))

        link_text = line2words(link.text())

        if len(title) + len (link_text) > sufficient_word_number:
            return title + link_text
        else:
            parent = PyQuery(link).parent ()
            while True:
                parent_words = line2words(parent.text ())
                if len (parent_words) < (sufficient_word_number - len(link_text) - len (title)): #should substract the link text part
                    #loop until the parent can cover the sufficient word number

                    if len(parent.parent ()) != 0: # parent exists, we can go further, or that's the best we can get
                        parent = parent.parent ()
                        continue
                        
                                                               
                siblings = recursive_contents(parent)#recursively get the contents
                
                index = siblings.index (link [0])#where the link is
                
                get_text = lambda e: line2words(isinstance (e, str) and str (e) or e.text) #get the text from the dom node, whether text node or element node
                

                prepending_words  = list(chain.from_iterable (map(get_text, siblings [:index]))) #words within the parent that prepend the link

                appending_words = list(chain.from_iterable (map(get_text, siblings [index+1:]))) #words within the parent that append the link
                
                remaining_number = sufficient_word_number - len(link_text) - len (title)
                
                #start the greedy search for words
                half_number = remaining_number / 2
                if len(prepending_words) >= half_number:
                    return prepending_words [-half_number: ] + title + link_text + appending_words [:half_number]
                elif len(prepending_words) < half_number: #to be made up by the appending words
                    left = remaining_number - len (prepending_words)
                    return prepending_words + title + link_text + appending_words [: left]
                else: #to be made up by the prepending words
                    left = remaining_number - len (apppending_words)
                    return prepending_words [-left:] + title + link_text + appending_words

        
    doc = PyQuery (doc)
    links = map(lambda link: (PyQuery(link).attr ('href'), get_link_words (link)), doc ("a"))
    
    #return them
    return links
