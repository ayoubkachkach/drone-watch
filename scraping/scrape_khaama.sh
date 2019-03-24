#!/usr/bin/env bash
PATH_TO_GECKO=$(pwd)
export PATH=$PATH:$PATH_TO_GECKO
python3.7 -m scrapy crawl dynamic_archive -a website_str=khaama -s JOBDIR=state/khaama_archive
