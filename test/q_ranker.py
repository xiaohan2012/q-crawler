import setting
import unittest

from src.q_ranker import Graph

class QRankerTest (unittest.TestCase):
    def test_propagation (self):
        from collections import namedtuple
        UrlInfo = namedtuple ('UrlInfo', 'url words') #handy tuple (url, words)
        
        sport = UrlInfo ('sport.com', ['sport',  'basketball',  'swimming'])
        ballgame = UrlInfo ('ball-game.com', ['ballgame', 'basketball', 'football'])
        basketball = UrlInfo ('basketball.com', ['nba', 'cba', 'yao'])
        nba = UrlInfo ('nba.com', ['nba', 'lbj', 'heat'])
        lbj = UrlInfo ('lbj.com', ['nba', 'star', 'heat'])
        
        g = Graph ()
        
        g.add_url(sport.url, sport.words, [ballgame.url])
        g.add_url(ballgame.url, ballgame.words, [basketball.url]) 
        g.add_url(basketball.url, basketball.words , [lbj.url, nba.url]) 
        g.add_url(nba.url, nba.words, [lbj.url]) 
        g.add_url(lbj.url, lbj.words, [nba.url])
        
        g.propagate (nba.url, 1, gamma = 0.7, level = 2, reached = (nba.url,))
        
        expected = [('nba', 2.89), ('heat', 1.7), ('cba', 1.19), ('yao', 1.19), ('lbj', 1), ('star', 0.7), ('basketball', 0.49), ('ballgame', 0.49), ('football', 0.49)]
        for word, score  in expected:
            self.assertAlmostEqual(g.word_score [word], score)



if __name__ == "__main__":
    unittest.main ()
