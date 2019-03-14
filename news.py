import requests


class Content:
    """
    Contains information on news articles.
    """

    def __init__(self, url, title, body):
        self.url = url
        self.title = title
        self.body = body

    def print(self):
        """
        Pretty printer for Content objects
        """
        print("URL: {}".format(self.url))
        print("TITLE: {}".format(self.title))
        print("BODY:\n {}".format(self.body))


class Newspaper:
    """
        Holds information on newspaper's structure for scraping.
    """

    def __init__(self, name, seed_urls, url_patterns, relative_url, title_class,
                 body_class, time_class, next_page):
        """
        Args:
            name (str) name of the newspaper.
            seed_urls (list of str) URLs to start scraping from.
            base_url (str) base url to use in case of relative urls.
            next_page (generator of str) returns next page to scrape.
            urls (list of str) seed URLs for scraping.
            target_patterns (list of regexp objects) regular expressions of links to follow during scraping.
            relative_url (bool) True if URLs in website are relative, False if they are absolute.
            title_class (str) CSS class of title.
            body_class (str) CSS class of body.
        """
        self.name = name
        self.url_patterns = url_patterns
        self.relative_url = relative_url
        self.title_class = title_class
        self.body_class = body_class
        self.time_class = time_class
        self.next_page = next_page
        self.seed_urls = seed_urls
