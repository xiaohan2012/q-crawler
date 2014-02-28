"""
The main program for q-crawler
"""
import q_ranker
from downloader import download
from scraper import scrape_url

def main (ranker, classifier, topic):
    """
    Given the starting URL seed list and the topical classifier and start crawling the web!
    """
    while len(ranker.unvisited_urls ()) != 0:#continue the process until the URL pool is exhausted
        
        #select from the pool that the URL has the highest Q-value/action value
        url = ranker.most_potential_url ()
        
        #fetch the page
        webpage, addition_info = download (url)
        
        print 'start crawling %s' %url
        if webpage == None: #invalid page encountered
            print 'failed to crawl %s. Reason: ' %(url), addition_info
            continue
        
        print 'crawled page %s' %url
        
        #scrape the urls
        urlinfo = scrape_url (webpage)
        
        #add the links to the graph
        ranker.add_links (map (lambda (dest_url, words): (url, dest_url, {'words': words}), urlinfo))

        #rate the webpage
        score = classifier.predict (webpage)
        print 'Classification result', score
        
        #update the Q function
        ranker.propagate (url, score [topic])
        

if __name__ == "__main__":
    from classifier import NBClassifier
    from q_ranker import QGraph
    from util import read_traindata
    
    #train the classifier, which could be cached actually
    classifier = NBClassifier ()
    classifier.train (read_traindata('unit_tests/data/train.txt'))
    
    seed_urls = ['http://www.python.org/', 'http://www.spam.com/'] #to be filled later
    g = QGraph (seed_urls)
    
    main (g, classifier, topic = 'spam')
