from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from spider.items import UrlItem
from spider.settings import START_URLS
from scrapy.http import Request

import os

from config import *

from classifier_util import read_classifier
from classifier import NBClassifier

from page_util import html2words
from scraper import scrape_url_and_words

class ApprenticeSpider(CrawlSpider):
    name = 'apprentice'
    start_urls = START_URLS
    
    rules = (
        Rule(SgmlLinkExtractor(unique=True), callback='parse_item', follow=True),#should it be unique 
    )
    
    print 'Loading supervisor...'
    print "path", os.path.join(DIRNAME, '../../../../data/classifier.pickle')
    supervisor = read_classifier (os.path.join(DIRNAME, '../../../../data/classifier.pickle'))
    print 'Supervisor loaded...'

    apprentice = NBClassifier ()
    
    def parse_item(self, response):
        """
        crawling the webpage and extracts the url.
        Once the crawling is done, evaluate the page content and enter this function again to train the apprentice
        """
            
        if response.meta.has_key ('train_flag') and response.meta ['train_flag']: #entering the train mode
            # print "training the apprentice"
            #html to words
            words = html2words (response.body)
            
            probs = ApprenticeSpider.supervisor.predict (words)
            
            interestness = probs ['pos']

            #use the score to train the apprentice using the surrouding (word, offset) pairs
            # print "word_offset_pairs = ", response.meta ['word_offset_pairs']
            # print "interestness of %s = %f" %(response.url, interestness)
            ApprenticeSpider.apprentice.train ([(response.meta ['word_offset_pairs'], interestness > 0.5 and "pos" or "neg")])
            
            item = UrlItem ()
            item ['url'] = response.url
            item ['interestness'] = interestness
            yield item

        else:
            # print "fetching the urls"
            url_infos = scrape_url_and_words (response.body, response.url, level=3)
            
            for url_info in url_infos:
                url, word_offset_pairs = url_info
                
                # print ApprenticeSpider.apprentice.predict (word_offset_pairs)
                
                prediction = ApprenticeSpider.apprentice.predict (word_offset_pairs)
                if prediction.has_key ('pos'):
                    potential_interestness = prediction['pos']#get the potential interest of the url
                else:
                    potential_interestness = 0#neg is 1
                
                # print "pi of %s is %f" %(potential_interestness, potential_interestness)

                priority = int(potential_interestness * 10**3)#converting the priority to int to accord with the PriorityQueue spec
                
                req = Request (url, priority = priority, callback = self.parse_item)#after the request is done, run parse_item to train the apprentice
                
                req.meta ['word_offset_pairs'] = word_offset_pairs #passing additional data to request
                req.meta ['train_flag'] = True #we only do training, nothing else
                yield req
            
        

    
