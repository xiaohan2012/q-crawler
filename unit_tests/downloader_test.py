import setting
import unittest

from src.downloader import download
from pyquery import PyQuery as pq

class DownloadTest (unittest.TestCase):

    def test_normal (self):
        url = 'http://example.com/'
        doc = download (url)
        title = pq (doc).find ('title').text ()
        print title
        self.assertTrue ('Example Domain', title)

    def test_404 (self):
        url = 'http://www.cs.helsinki.fi/u/hxiao/rl-seminar/paper.pd'
        nil, err_code = download (url)
        self.assertEqual (nil, None)
        self.assertEqual (err_code, 404)

    def test_nonhtml (self):
        url = 'http://www.cs.helsinki.fi/u/hxiao/rl-seminar/paper.pdf'
        nil, err_msg = download (url)
        self.assertEqual (nil, None)
        self.assertEqual (err_msg, 'application/pdf')

if __name__ == "__main__":
    unittest.main ()
        
