Q-crawler
===========

[![Build Status](https://travis-ci.org/xiaohan2012/q-crawler.png?branch=master)](https://travis-ci.org/xiaohan2012/q-crawler)

*Reinforcement learning* based Focused Web crawler, which aims at crawling on-topic webpages more efficiently by learning via the process of crawling

#Usage


##Before you run

In order to crawl webpages of given topics, it is necessary to define the topic.

In this context, topic can be defined by providing labeled webpages, each of which are either labled as positive (on-topic) or negative (off-topic).

This corpus preparation process is done in the following procedure:

1. collect webpages and label each of them as either positive or negative
2. use the utility script `pages2word.sh` to convert webpages to bag of words
3. group the page words by their labels and aggregate each group into one single file (format to be specified below), such as `pos` for the positive webpages and `neg` for the negative ones.
4. put the `pos` and `neg` corpus file under the `data/` directory

Each webpage occupies one line, containing the words separated by `\t` and a lable, either `pos` or `neg` is appended to the tail, with a `\t` preceding it. 

Such example is:


```
word1\tword2\tword3\tpos
word3\tword4\tword5\tneg
```

##Run the software


#Methodology

##Supervisor&Apprentice Model

- Supervisor: classifier that rates the relativeness of acquired webpage
- Apprentice: another classifier that uses the above feedback to learn what kind of urls are more likely to lead to valuable webpages

##Why Reinforcement learning?


##URL representation

It is intuitive to represent the URLs as its anchor terms together with its surroudning terms.

In addition, q-cralwer incorporates each term's *offset* to the link, its DOM-distance to the link. 

The intuition is: terms that are of different distance in terms of DOM structure should be considered differently. For example, anchor text should tell more about the URL while surrounding text are less predictive.


#Experiment

Two crawlers, one baseline crawler, the other the apprentice-based crawler are compared in terms of the ability to crawl ontopic webpages efficiently.
