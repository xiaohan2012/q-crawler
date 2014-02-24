"""
The main program for q-crawler
"""
import q_ranker
from downloader import download
from scraper import scrape

def main (pool, classifier):
    """
    Given the starting URL seed list and the topical classifier and start crawling the web!
    """

    while pool.isEmpty ():#continue the process until the URL pool is exhausted
        
        #select from the pool that the URL has the highest Q-value/action value
        url = q_ranker.most_potential_url (pool)

        #fetch the page
        webpage = download (url)

        if webpage == None: #invalid page encountered
            continue
        
        #scrape the urls
        urls = scrape (webpage)
        
        #rate the webpage
        score = classifier.rate (webpage)
        
        #update the Q function
        q_ranker.update (url, webpage, score)
        
        #add the urls to the pool
        pools.add (urls)

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
