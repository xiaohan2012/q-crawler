import setting
import unittest

from src.q_ranker import Graph

class QRankerTest (unittest.TestCase):
    def setUp (self):
        from collections import namedtuple
        UrlInfo = namedtuple ('UrlInfo', 'url words') #handy tuple (url, words)
        
        sport = UrlInfo ('sport.com', ['sport',  'basketball',  'swimming'])
        ballgame = UrlInfo ('ball-game.com', ['ballgame', 'basketball', 'football'])
        basketball = UrlInfo ('basketball.com', ['nba', 'cba', 'yao'])
        nba = UrlInfo ('nba.com', ['nba', 'lbj', 'heat'])
        lbj = UrlInfo ('lbj.com', ['nba', 'star', 'heat'])

        #unvisited urls
        wade = UrlInfo ('wade.com', ['nba', 'wade', 'heat'])
        sexygirl = UrlInfo ('sexygirl.com', ['nba', 'sexy', 'girl'])
        
        g = Graph ()
        
        g.add_url(sport.url, sport.words, [ballgame.url])
        g.add_url(ballgame.url, ballgame.words, [basketball.url]) 
        g.add_url(basketball.url, basketball.words , [lbj.url, nba.url]) 
        g.add_url(nba.url, nba.words, [lbj.url, 
                                       wade.url, sexygirl.url #unvisited ones
                                   ]) 
        g.add_url(lbj.url, lbj.words, [nba.url])

        g.add_url(wade.url, wade.words, [])
        g.add_url(sexygirl.url, sexygirl.words, [])

        self.g = g
        
        #propagate the rewards
        g.propagate (nba.url, 1, gamma = 0.7, level = 2, reached = (nba.url,))
        
    def test_propagation (self):
        """
        test what word scores resulted from the progagation 
        """
        expected = [('nba', 2.89), ('heat', 1.7), ('cba', 1.19), ('yao', 1.19), ('lbj', 1), ('star', 0.7), ('basketball', 0.49), ('ballgame', 0.49), ('football', 0.49)]
        for word, score  in expected:
            self.assertAlmostEqual(self.g.word_score [word], score)

    def test_url_scores (self):
        """
        url scores for urls
        """
        scores = self.g.url_scores (['wade.com', 'sexygirl.com'])
        expected = {'wade.com': 2.89 + 1.7, 'sexygirl.com': 2.89}
        
        for url, score  in expected.items ():
            self.assertAlmostEqual (score, scores [url])
        
    def test_unvisited_urls (self):
        """
        get all out-degree=0 nodes
        """
        expected = {'wade.com', 'sexygirl.com'}
        self.assertEqual (set(self.g.unvisited_urls ()), expected)
        
    def test_most_potential_url (self):
        """
        the url with the highest score
        """
        best_url = self.g.most_potential_url ()
        self.assertEqual (best_url, 'wade.com')
        
        
if __name__ == "__main__":
    unittest.main ()
