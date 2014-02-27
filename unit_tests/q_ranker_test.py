import setting
import unittest

from src.q_ranker import Graph

class QRankerTest (unittest.TestCase):
    def setUp (self):
        from collections import namedtuple

        sport = 'sport.com' 
        ballgame = 'ball-game.com' 
        basketball = 'basketball.com' 
        nba = 'nba.com' 
        lbj = 'lbj.com' 
        #unvisited urls
        wade = 'wade.com'
        sexygirl = 'sexygirl.com'
        #unralted site
        porn = 'porn.com'
        
        links = [(sport, ballgame, {'words':  ['ballgame', 'basketball', 'football']}),
                 (ballgame, basketball, {'words': ['nba', 'cba', 'yao']}),
                 (basketball, nba, {'words': ['nba', 'association', 'basketball']}),
                 (nba, lbj, {'words': ['nba', 'lbj', 'heat']}),
                 (nba, wade, {'words': ['nba', 'star', 'heat']}),
                 (nba, sexygirl, {'words': ['nba', 'sexy', 'girl']}),
                 (porn, sexygirl, {'words': ['oral', 'sex', 'asian']}),
                 (lbj, nba, {'words': ['nba', 'player', 'heat']}),
                 (basketball, lbj, {'words': ['nba', 'player', 'miami']})]
        
        g = Graph ()
        
        g.add_links (links)
        
        self.g = g
        
        #propagate the rewards
        g.propagate (nba, 1, gamma = 0.7, level = 2, reached = (nba,))
        
    def test_propagation (self):
        """
        test what word scores resulted from the progagation 
        """
        expected = [('nba', 3.4), ('player', 1.7), ('heat', 1), ('basketball', 1), ('association', 1), ('miami', 0.7), ('cba', 0.7), ('yao', 0.7)]
        for word, score  in expected:
            self.assertAlmostEqual(self.g.word_score [word], score)

    def test_url_scores (self):
        """
        url scores for urls
        """
        scores = self.g.url_scores (['wade.com', 'sexygirl.com'])
        expected = {'wade.com': 3.4 + 1, 'sexygirl.com': 1.7}
        
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
