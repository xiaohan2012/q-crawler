"""
The document classifier that gives the probability that a document belongs to a given topic
"""

from __future__ import division
from itertools import groupby
from collections import Counter

class Classifier ():
    """
    The classifier
    """
    def train (self):
        raise NotImplementedError
        
    def rate (self):
        raise NotImplementedError

class NBClassifier (Classifier):
    
    def train (self, texts, rare_threshold = 1):
        """
        train the Naive Bayes model
        
        texts: the list of (document, label) 
        rare_threshold: what is the minimum frequency of words that we would not consider it as rare
        
        Return: None

        
        """

        #compute the prob table for classes, class frequencies

        clsFreq = Counter (map (lambda (t, cls): cls, texts))

        pt = {}
        for cls in clsFreq.keys ():
            pt [cls] = clsFreq [cls] / sum(clsFreq.values ())

        self.classes = pt.keys () #the classes

        #the vocabulary containing all the words sorted by alphabetical order
        vocabulary = sorted(list(set([w for words,cls in texts for w in words])) + ['__RARE__'])

        #compute the CPD
        #group texts by class
        textsGroupedByCls = groupby (sorted (texts, key = lambda tpl: tpl [1]), lambda tpl: tpl [1])

        cpd = {}

        #for each class
        for cls, listOfTexts in textsGroupedByCls:
            cpd [cls] = {}
            
            #count the frequency of each word
            wordFreqRaw = Counter([w for ts, cls in listOfTexts for w in ts])

            #filter out those whose frequency < rare_threshold 
            #and aggragate those rare words' frequency
            wordFreq = Counter ()
            for w in wordFreqRaw:
                    
                if wordFreqRaw [w] < rare_threshold:
                    wordFreq ["__RARE__"] += wordFreqRaw [w]
                else:
                    wordFreq [w] = wordFreqRaw [w]

            totalCount = sum(wordFreq.values ())
            
            #for each word in the vocabulary, calcualte the relative frequency (with smoothing)
            for w in vocabulary:
                cpd [cls][w] = (wordFreq [w] + 1) / (totalCount + len (vocabulary))
                
        self.pt = pt
        self.cpd = cpd

    def predict (self, words):
        """
        Give the probability that the document is classified as positive
        
        words: list of word (str)

        Return: list of (class, the probability) in ascending order by the probability
        """
        probs = {}
        total = 0
        for cls in self.classes:
            #if rare words are seen, use the __RARE__ item
            probs [cls] = reduce (lambda acc, word: acc * self.cpd [cls] [word if self.cpd [cls].has_key (word) else '__RARE__'] , words, self.pt [cls])
            total += probs [cls]
            
        #normalization
        for cls in self.classes:
            probs [cls] /= total
            
        return sorted(probs.items (), key=lambda p: p [1], reverse = True)
        
        
