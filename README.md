Q-crawler
===========

[![Build Status](https://travis-ci.org/xiaohan2012/q-crawler.png?branch=master)](https://travis-ci.org/xiaohan2012/q-crawler)

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

1. Surrouding text of the url
2. The title of the url
3. The display text of the url

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




