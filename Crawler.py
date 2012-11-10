#!/usr/bin/python
from BeautifulSoup import *
import json
import os, sys, urllib2

"""
    Used by Redback to grab HTML.
"""
class Crawler:

    def __init__(self, raw_html_dict = {}, links_dict = {}, headers_dict = {}):
        """
            Takes dicts for holding page => HTML and page => hrefs
        """
        self.raw_html_dict = raw_html_dict
        self.links_dict = links_dict
        self.headers_dict = headers_dict 

    def crawl(self, page):
        """
            Recursively move through links until there are none left.
            Add HTML to raw_html_dict and valid href tags to links_dict
        """

        # Validate html and file extension
        if 'http://' not in page:
            page = 'http://' + page
        
        #if ('doc' in page or 'pdf' in page or 'mailto' in page):
        #    return
    
        # Try to get HTML, read if successful
        try:
            message = urllib2.urlopen(page)
        except urllib2.HTTPError as e:
            print e
            return
        rawHTML = message.read()

        # Stow header away for later
        self.headers_dict[page] = str(message.info())

        # Stick raw HTML into dict and use BS
        self.raw_html_dict[page] = rawHTML
        links = self.parse_html(rawHTML, page, 'a', 'href', ['#'])

        # Add links not yet in master link collection recursively
        if page in self.links_dict:
            return
        else:
            self.links_dict[page] = links
            for link in links:
                self.crawl(link)

    def parse_html(self, rawHTML, page, tag, attribute, excluded):
        """
            Takes raw HTML and page's name as strings.
            Takes HTML tag and attribute values as strings.
            Takes a list of any strings that should be excluded.
            Returns a list of all tags with specified attribute found in HTML.
        """
        x = [str(i.get(attribute)) for i in BeautifulSoup(rawHTML)(tag)] 
        return [self.get_absolute_path(l, page) for l in x if not any(e in l for e in excluded)]

    def get_absolute_path(self, link, path):
        """
            Takes relative path.
            Returns absolute path to root of website.
        """

        pathList = path.split('/')
        while '..' in link:
            pathList.pop()
            link = link.partition('..')[2]
        link = link.replace('./','/')

        # return absolute path
        return '/'.join(pathList) + link

# End of Crawler.py

