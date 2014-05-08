all: html stat
	chmod a+r ~/public_html/rl-project/*

html:
	chmod -R a+x ~/public_html/rl-project
	cp comparison.html ~/public_html/rl-project/

stat:
	python gen_html_data.py
	cp data/python/apprentice_stat.js ~/public_html/rl-project/apprentice.json
	cp data/python/baseline_stat.js ~/public_html/rl-project/baseline.json
