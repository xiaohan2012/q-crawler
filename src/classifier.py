"""
The document classifier that gives the probability that a document belongs to a given topic
"""

from __future__ import division
import math
from itertools import groupby
from collections import Counter, defaultdict

class Classifier ():
    """
    The classifier
    """
    def train (self):
        raise NotImplementedError
        
    def rate (self):
        raise NotImplementedError

class NBClassifier (Classifier):
    """
    The Naive Bayes classifier
    """
    def __init__ (self):
        self._label_freq = Counter ()
        self._feature_freq = defaultdict (Counter) #the counter for features under different labels
        self._vocabulary = set (['__RARE__'])
        
        self._classes = None
        self.pt = None
        self.cpd = None

    def label_freq (self):
        return self._label_freq
        
    def feature_freq (self):
        return self._feature_freq

    def labels(self):
        return self._classes

    def vocabulary(self):
        return self._vocabulary
        
    def train (self, texts, rare_threshold = 1):
        """
        train the Naive Bayes model incrementally (based on previous training results)
        
        texts: the list of (document, label) 
        rare_threshold: what is the minimum frequency of words that we would not consider it as rare
        
        Return: None
        """

        #compute the prob table for classes, class frequencies
        label_freq = Counter (map (lambda (t, cls): cls, 
                                   texts))
        
        pt = {}
        for cls in label_freq.keys ():
            #update the total number
            self._label_freq [cls] += label_freq [cls]
            
        for cls in label_freq.keys ():
            #compute the prior
            pt [cls] = self._label_freq [cls] / sum(self._label_freq.values ())
        
        self._classes = pt.keys () #the classes

        #the vocabulary containing all the words sorted by alphabetical order
        self._vocabulary =  self._vocabulary.union(set([w for words,cls in texts for w in words]))

        #compute the CPD
        #group texts by class
        textsGroupedByCls = groupby (sorted (texts, key = lambda tpl: tpl [1]), lambda tpl: tpl [1])

        cpd = {} #the conditional probability table
        
        #for each class
        for cls, listOfTexts in textsGroupedByCls:
            cpd [cls] = {}
            
            #count the frequency of each word
            wordFreqRaw = Counter([w for ts, cls in listOfTexts for w in ts])

            #filter out those whose frequency < rare_threshold 
            #and aggragate those rare words' frequency

            for w in wordFreqRaw:
                    
                if wordFreqRaw [w] < rare_threshold:
                    self._feature_freq [cls] ["__RARE__"] += wordFreqRaw [w]
                else:
                    self._feature_freq [cls] [w] += wordFreqRaw [w]
            
            totalCount = sum(self._feature_freq [cls].values ())
            
            #for each word in the vocabulary, calcualte the relative frequency (with smoothing)
            for w in self._vocabulary:
                cpd [cls][w] = (self._feature_freq [cls] [w] + 1) / (totalCount + len (self._vocabulary))
                
        self.pt = pt
        self.cpd = cpd        

    def predict (self, words):
        """
        Give the probabilities that the document belongs to each topic (**using log exp trick**)
        
        words: list of word (str)

        Return: list of (class, the probability) in ascending order sorted by the probability
        """
        get_log_prob = lambda cls, word: math.log(self.cpd [cls] [word if self.cpd [cls].has_key (word) else '__RARE__']) #handy function that gives log(P (word|cls))
        
        log_probs = {}
        for cls in self._classes:
            #if rare words are seen, use the __RARE__ item
            log_probs [cls] = reduce (lambda acc, word: acc + get_log_prob (cls, word), words, math.log(self.pt [cls]))
            
        B = max (log_probs.values ())
        total = math.log (sum (map (lambda b_c: math.exp (b_c - B), log_probs.values()))) + B
        
        return dict(map (lambda (cls, log_prob): (cls, math.exp(log_prob - total)),  log_probs.items ()))        
        
