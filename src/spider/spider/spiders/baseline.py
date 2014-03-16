from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from spider.items import UrlItem
from scrapy.http import Request

import os

from config import *

from classifier_util import read_classifier
from classifier import NBClassifier

from page_util import html2words
from scraper import collect_urls

class BaselineSpider(CrawlSpider):
    name = 'baseline'
    start_urls = ['http://www.bbc.com/news/']
    
    rules = (
        Rule(SgmlLinkExtractor(unique=True), callback='parse_item', follow=True),
    )

    print 'Loading classifier...'
    print "path", os.path.join(DIRNAME, '../../../../data/classifier.pickle')
    classifier = read_classifier (os.path.join(DIRNAME, '../../../../data/classifier.pickle'))
    print 'Classifier loaded...'
    
    def parse_item(self, response):
        #if this page is of interest (according to the NB classifier prediction result), 
        # then add all its links to pool, 
        # each of which the priority is the probability score
        
        #html to words
        words = html2words (response.body)

        probs = BaselineSpider.classifier.predict (words)
        
        interestness = probs ['pos']
        #print 'Interestness of [%s]= %.4f' %(response.url, interestness)
        
        if interestness > .5:
            #print "Collect all the urls as it is interesting"
            urls = collect_urls (response.body, response.url)
            for url in urls:
                priority = int(interestness * 10**3)#converting the priority to int to accord with the PriorityQueue spec
                yield Request (url, priority = priority) #added to the pool
        else:
            pass
            #print 'Skipping as it is not interesed at all'
        
        
        item = UrlItem ()
        item ['url'] = response.url
        item ['interestness'] = interestness
        yield item
