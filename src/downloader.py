"""
The downloader that downloads the webpage and scrapes the (URL, surrounding text)
"""
import urllib2

def download (url):
    """
    Download the webpages only in the format of HTML 
    url: str
    
    Return: the document or None if exception happens
    """
    
    #download the page
    try: 
        res = urllib2.urlopen(url)
    except urllib2.HTTPError as err:
        return None, err.code

    if res.headers.type.lower () == 'text/html':
        return res.read(), None
    else:
        return None, res.headers.type.lower ()
    
