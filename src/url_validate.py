"""
url validator
"""

from urlparse import urlparse

def is_valid (url):
    """
    at least the host should be known
    """
    r = urlparse (url)
    if len(r.netloc) > 0:
        return True
    return False
    
