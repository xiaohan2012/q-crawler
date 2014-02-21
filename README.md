Q-crawler
===========

*Reinforcement learning* based Focused Web crawler by improving the Q-function


#Introduction

##Reinforcement learning elements

1. State space: only one (thus, only one type of state transition)
2. Action space: fetch some URL(distinguished by the bag-of-words about it on the webpage)
3. Reward function: the score/probability assigned by a topic classifier
4. Q function: bag-of-words -> numerical reward mapping

The webpage its received can be analysed (does the link representation says a lot about the webpage's topic) and used to update the Q function.

#Crawling work flow

Input: a URL pool intialized with seed URLs and a topical classifier

1.  get the URL that has the highest Q value and fetch the page.
2.  strip all the html tags except `<a></a>` and link all the URLs within the page.
3.  analyze the page extract the main content, rate it using the classifier and associate it with the URL's bag-of-words to update the Q function(And even the classifier!).
4.  associate each URL with the surrouding words.
5.  save new URLs with their surrounding words into the URL pool.
6.  return to step **1**.


#Bag-of-words of the URL

Through several informative places, some hints about what webpage behind the URL might be about can be found through:

1. The sentence that contains the link
2. The title of the link
3. The display text of the link
4. Of course, tags that comes from social bookmarking/tagging system

##Sentence

If the sentence is too short, then probably one or more sentence(s) preceding or appending it gives hint on what the URL is about.

Simple rules:

1. If the sentence is more than or equal to 10 words, then we assume only this sentence is about the URL
2. Else if the sentence is less than 10 words and greater than 5 words and the preceding or appending sentence (if exist) does not contain link, then we assume the preceding or appending sentence belongs to the URL.
3. Else if the sentence is less than 5 words and the preceding or appending two sentences (if exist) does not contain link, then we assume the preceding or appending sentences belong to the URL.

*Note*: Can I build a classifier that segments this sentences according to which URL it is talking about?

##Title

The title should be contribute itsself completely to the description about the URL

##Link text

Same case as the previous one

#Classifier

The classifier is training using a set of webpages/text that are about a specific topics (e.g, Python) plus a random set of off-topic pages. And the input it receives is a set of words and output the probability that it belongs to that topic.

*Note*: Can I simply this part? Maybe use some available classifier?

#Q-function

Q-function is an approximation of the future reward that taking a specific action will yield.

It receives a bag of words and output a numerical value.


##Calculation
Assuming each term contributes independently to the "topicness", then each term will be assigned a numerical value about its contribution.

Given the bag of words, it simply sums up the corresponding numerical contributions or *weight*.
	
##Backpropagation

Once we found a good webpage (e.g, Python), the terms in which webpages (e.g, some programming forum) that point to the useful page should be given some increase/reward.

We assume terms in webpages which are within distance of 5 are rewarded.

##Normalization

To bound the term weight, they are normalized after each Q-function update.




