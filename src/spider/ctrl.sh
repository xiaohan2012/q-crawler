#! /bin/sh
rm data/python/*
scrapy crawl -L INFO apprentice -o data/python/urls-apprentice.json -t json
scrapy crawl -L INFO baseline -o data/python/urls-baseline.json -t json

