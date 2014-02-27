"""
The main program for q-crawler
"""
import q_ranker
from downloader import download
from scraper import scrape

def main (classifier, q_ranker):
    """
    Given the starting URL seed list and the topical classifier and start crawling the web!
    """

    while len(q_ranker.unvisited_urls ()) == 0:#continue the process until the URL pool is exhausted
        
        #select from the pool that the URL has the highest Q-value/action value
        url, words = q_ranker.most_potential_url ()

        #fetch the page
        webpage = download (url)
        
        print 'start crawling %s' url
        if webpage == None: #invalid page encountered
            print 'failed to crawling %s' url
            continue
        
        print 'crawled page %s' %url
        
        #scrape the urls
        urlinfo = scrape (webpage)
        
        #add the link pairs to the graph
        q_ranker.add_url (url, urlinfo)

        #rate the webpage
        score = classifier.predict (webpage)
        print 'Relevance score: %.4f' %score
        
        #update the Q function
        q_ranker.progapate (url, webpage, score)
        

if __name__ == "__main__":
    from classifier import NBClassifier, read_trainset
    from url_pool import URLPool
    from util import read_trainset
    
    #train the classifier, which could be cached actually
    classifier = NBClassifier ()
    classifier.train (read_trainset(data))
    
    seed_urls = [] #to be filled later
    pool = URLPool (seed_urls)
    
    main (seend_urls, NBclassifier)
