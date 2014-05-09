Q-crawler
===========

[![Build Status](https://travis-ci.org/xiaohan2012/q-crawler.png?branch=master)](https://travis-ci.org/xiaohan2012/q-crawler)

#Preparation

##Virtual environment
Run
```
cd q-crawler
virtualenv venv
```
to setup the virtual environment.

Run 
```
source venv/bin/activate
```
to ensure the virtual environment is activated.

##Dependency resolving
```
pip install -r requirements.txt
```
Be patient. It might take several minutes.

You may encounter the error:  `/bin/sh: xslt-config: not found`. Please see this [post](http://stackoverflow.com/questions/5178416/pip-install-lxml-error) for solution.

#Run the demo

To see how the RL-based crawler compares to the baseline crawler(the ordinary one), run the following command

```
cd src/spider
./ctrl.sh %run the crawler and feel free to have a cup of coffee during the crawling :)
python gen_html_data.py
```

Last, open the `comparison.html` file using Web browser to see the performance comparison.

The crawling process might run 15~20 minutes, varied by the Internet connection speed.

If you want to speed up the process, the number of URLs to be crawled can be changed(default to 10000). See [configuration](https://github.com/xiaohan2012/q-crawler/#configuration).

#Usage

##training

```
cd src
python classifier_util.py train
```

And the produced classifier will be pickled and put in `data/classifier.pickle`.

##crawling

```
cd src/spider
scrapy crawl apprentice 
scrapy crawl baseline
```

##Performance monitoring

```
cd src/spider
python gen_html_data.py
```

Open the `comparison.html` using modern web browser(Firefox 24.4.0 tested OK).

Some example performance plot is [here](http://www.cs.helsinki.fi/u/hxiao/rl-project/comparison.html).

##Training data preprocessing 

Merge the positive/negative training samples into two separate files, each for one class. Each line represents one traing sample and consists of the tokens in the sample and is ended with class label of the sample(`pos` or `neg`).

Put both files under the `data` directory. Name the postive sample files to `pos` and negative sample files to `neg`.

See [this(for negative samples)](https://raw.githubusercontent.com/xiaohan2012/q-crawler/master/data/neg) and [this(for positive samples)](https://raw.githubusercontent.com/xiaohan2012/q-crawler/master/data/pos) files for example.

##Configuration

1. Maximum number of crawled URLs: change  `CLOSESPIDER_ITEMCOUNT`'s value in [this](https://github.com/xiaohan2012/q-crawler/blob/master/src/spider/spider/settings.py) file
2. Starting URLs: change`START_URLS`'s value in [this](https://github.com/xiaohan2012/q-crawler/blob/master/src/spider/spider/settings.py) file

#Contact
xiaohan2012 at gmail.com

