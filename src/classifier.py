"""
The document classifier that gives the probability that a document belongs to a given topic
"""
class Classifier ():
    """
    The classifier
    """
    def train (self):
        raise NotImplementedError
        
    def rate (self):
        raise NotImplementedError

class NBClassifier (Classifier):
    
    def train (self, rows):
        """
        train the Naive Bayes model
        
        rows: the list of (document, label) 
        
        Return: None
        """

    def predict (self, words):
        """
        Give the probability that the document is classified as positive
        
        words: list of word (str)

        Return: the probability the document is positive
        """
        
