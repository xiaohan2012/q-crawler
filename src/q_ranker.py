"""
The URL ranker based on Q-function
Essentially, it gives each term a 
"""

import networkx as nx
from collections import defaultdict

class QGraph (nx.DiGraph):
    """
    A Graph where nodes are the urls and edges are the links
    """
    def __init__ (self, initial_urls = []):
        self.word_score = defaultdict (int) #the weight for each word
        self.backlinks = defaultdict (list) #the backlink map
        
        
        super(QGraph, self).__init__()
        
        #add the initial urls
        self.add_nodes_from (initial_urls)
        
    def add_links (self, links):
        """
        add links to the graph and record the backlink
        
        src_url: url that points to the urlinfo
        urlinfo: urlinfo to be added
        """
        self.add_edges_from(links)
                
        for src_url, dest_url, _ in links:
            self.backlinks [dest_url].append (src_url)
            
    def get_back_links (self, url):
        """
        the urls that point to `url`
        """
        return self.backlinks [url]
        
    def propagate (self, url, score, gamma=0.7, level=3, reached = () ):
        """
        url: the starting url to propagate 
        score: the relevance score of the url
        gamma: the discounting rate
        level: the distance for propagation
        reached: ancestors that propagates the reward to this url

        This function propagates the score/reward of the webpage to its backlinks
        """
        if level >= 1: #within the progagating distance
            #add the score for current url's words
            node = self.node [url]

            #get the webpage's backlinks and filter out those ancetors as propagating back the reward is not permitted
            backurls = filter(lambda u: u not in reached, self.get_back_links (url))
            
            #recursively propagate the discounted score
            for back_url in backurls:
                #get the link
                words = self.edge [back_url][url] ['words']

                #update the word sore
                for word in words:
                    self.word_score [word] += score
                    
                #the link receives the reward and add distribute them back to the words
                self.propagate (back_url, gamma * score, gamma, level - 1, reached + (back_url, ))
                
    def unvisited_urls (self):
        """
        nodes whose outdegree is zero
        """

        return map (lambda (url, _): url, filter(lambda (_,degree): degree == 0, self.out_degree_iter ()))
        
    def url_scores (self, urls):
        """
        return dict of (url, score)
        """
        #function the map words to score
        words_score = lambda words: sum(map (lambda w: self.word_score [w], words))
        
        #function get url score
        def url_score (url):
            #the mean score calculated from all links that point to it
            if len (self.backlinks [url]) == 0: #no backlinks, the inital seed?
                return 0
            else:
                return sum(map(lambda back_url: words_score(self.edge [back_url] [url] ['words']), self.backlinks [url])) / len (self.backlinks [url])
        
        #for each url, get links that point to it
        return dict(map (lambda url: (url, url_score(url)), urls))

    def most_potential_url (self):
        """
        For those unvisited urls (those pointing to nothing), return the most potential one
        Return:
        the url with the highest ranking score and its surrounding words
        """
        #get the unvisited urls
        urls = self.unvisited_urls ()
        
        scores = self.url_scores (urls)

        #rank the score of each url in the graph        
        url = max( urls, key=lambda url: scores [url])

        return  url
