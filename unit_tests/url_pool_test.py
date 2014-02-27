import setting
import unittest

from src import url_pool

class URLPoolTest (unittest.TestCase):
    def test_add (self):
        dup_url = 'http://www.yolamda.net/'; new_url = 'http://www.screwgunrecords.com/'
        
        init_urls = ['http://www.lovelessrecords.com/',
                     'http://www.virtualkiss.com/', dup_url]

        pool = url_pool.URLPool (init_urls)
        
        pool.add ([dup_url, new_url])
        expected = init_urls + [new_url]

        self.assertEqual(list(pool), expected)

if __name__ == "__main__":
    unittest.main ()
