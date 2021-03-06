# Scrapy settings for spider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'spider'

SPIDER_MODULES = ['spider.spiders']
NEWSPIDER_MODULE = 'spider.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'spider (+http://www.yourdomain.com)'

ITEM_PIPELINES = {
    'spider.pipelines.UrlPipeline': 300,
}


CLOSESPIDER_ITEMCOUNT=10000 #crawling only 10000 pages

START_URLS = ['https://www.python.org/',
              'http://stackoverflow.com/',
              'http://www.bbc.com/']
