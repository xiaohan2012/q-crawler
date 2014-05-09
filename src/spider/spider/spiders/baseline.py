from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from spider.items import UrlItem
from spider.settings import START_URLS
from scrapy.http import Request

import os

from config import *

from classifier_util import read_classifier

from page_util import html2words
from scraper import collect_urls

class BaselineSpider(CrawlSpider):
    name = 'baseline'
    start_urls = START_URLS
    
    rules = (
        Rule(SgmlLinkExtractor(unique=True), callback='parse_item', follow=False),
    )
    crawled_urls = []
    
    print 'Loading classifier...'
    print "path", os.path.join(DIRNAME, '../../../../data/classifier.pickle')
    classifier = read_classifier (os.path.join(DIRNAME, '../../../../data/classifier.pickle'))
    print 'Classifier loaded...'
    
    def parse_item(self, response):
        #we must do the manual URL collection work as the priority should be defined by us!
        BaselineSpider.crawled_urls.append(response.url)
        
        #html to words
        words = html2words (response.body)

        probs = BaselineSpider.classifier.predict (words)
        
        interestness = probs ['pos']
        #print 'Interestness of [%s]= %.4f' %(response.url, interestness)
        
        # if response.meta.has_key ('add_item_flag') and response.meta ['add_item_flag']:
        item = UrlItem ()
        item ['url'] = response.url
        item ['interestness'] = interestness
        yield item
        # else:
        urls = collect_urls (response.body, response.url)
        for url in urls:
            if url in BaselineSpider.crawled_urls:
                continue
            priority = int(interestness * 10**3)#converting the priority to int to accord with the PriorityQueue spec
            req = Request (url, priority = priority, callback = self.parse_item)
            yield req#added to the pool                    
