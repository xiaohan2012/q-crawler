# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class UrlPipeline(object):
    def process_item(self, item, spider):
        with open ('data/python/urls.txt', "a") as f:
            f.write ("%s\t%f\n" %(item ['url'], item ['interestness']))
        return item
