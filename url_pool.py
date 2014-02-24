"""
The URL pool
"""

class URLPool (list):
    def add (self, new_urls):
        #get urls not in this list
        new_urls = filter (lambda url: url not in self, new_urls)

        #add them to the current pool
        self.extend (new_urls)
