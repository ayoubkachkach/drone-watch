Web app that scrapes online articles and automatically classifies which ones are reporting on drone airstrikes or not. The articles reporting on drone strikes can be further labelled. The labels are stored in a DB for further analysis.

Run drone-watch/scraping/scrape_all.py to scrape all supported websites!

Adding new sources to scrape should be made by adding a new instance of Website in /scraping/website.py and adding it to the dict 'websites'. 
