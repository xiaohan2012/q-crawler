Q-crawler
===========

[![Build Status](https://travis-ci.org/xiaohan2012/q-crawler.png?branch=master)](https://travis-ci.org/xiaohan2012/q-crawler)

#Installation

`>>git clone`

`>>pip install -r requirements.txt`

#Run the demo

#Usage

##training

`>> cd src`

`>> python classifier_util.py train`

##crawling
`>> cd src/spider`

`>> scrapy crawl apprentice %for the reinforcement learning based crawler`

`>> scrapy crawl baseline %for the reinforcement learning based crawler`

##Performance monitoring

`>> cd src/spider`

`>> make`

Open the `comparison.html` using modern web browser(Firefox 24.4.0 tested OK).

Some example performance plot is [here](http://www.cs.helsinki.fi/u/hxiao/rl-project/comparison.html).

##Training data preprocessing 

##Configuration

1. Maximum number of crawled URLs: change  `CLOSESPIDER_ITEMCOUNT`'s value in [this](https://github.com/xiaohan2012/q-crawler/blob/master/src/spider/spider/settings.py) file
2. Starting URLs: change`START_URLS`'s value in [this](https://github.com/xiaohan2012/q-crawler/blob/master/src/spider/spider/settings.py) file

#Contact
xiaohan2012 at gmail.com
