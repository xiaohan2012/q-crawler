"""
The URL ranker based on Q-function
Essentially, it gives each term a 
"""

import networkx as nx
from collections import defaultdict

class Graph (nx.DiGraph):
    """
    A Graph where nodes are the urls and edges are the links
    """
    def __init__ (self):
        self.word_score = defaultdict (int) #the weight for each word
        self.backlinks = defaultdict (list) #the backlink map

        super(Graph, self).__init__()
        
    def add_url (self, url, words, dest_urls = []):
        """
        add (url, dest_url) pairs to the graph
        """

        self.add_node (url, words = words)

        self.add_edges_from (map (lambda dest_url: (url, dest_url), dest_urls))
        
        for dest_url in dest_urls:
            self.backlinks [dest_url].append (url)
        
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
        if level >= 0: #within the progagating distance
            

            #add the score for current url's words
            node = self.node [url]

            for word in node ['words']:
                self.word_score [word] += score

            #get the webpage's backlinks and filter out those ancetors as propagating back the reward is not permitted
            backurls = filter(lambda u: u not in reached, self.get_back_links (url))
            
            #recursively propagate the discounted score
            for back_url in backurls:
                #the link receives the reward and add distribute them back to the words
                self.propagate (back_url, gamma * score, gamma, level - 1, reached + (back_url, ))

    def most_potential_url (self, urls):
        """
        urls: list of  (URL string, surrouing text)
        
        Return:
        the url with the highest ranking score
        """
        