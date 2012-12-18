#!/usr/bin/python

"""
    Given FQDN/IP, scans for vulnerable pages and parameters.

"""
from BeautifulSoup import BeautifulSoup    
import urllib2

class Scanner:
    def __init__(self):
        """
            :pages: Memo for pages already crawled.
        """
        self.pages = {}

    def page(self, page):
        """ Grab page with urllib and split on whitespace.
            :throws: HTTPError.
            :returns: list representing page's text
        """
        if 'http://' not in page:
            page = 'http://' + page
    
        # Memoize for efficiency and stealth.
        if page in self.pages:
            return self.pages[page]

        # Try to get HTML, read if successful
        try:
            html = urllib2.urlopen(page).read()
            message = '\n'.join(BeautifulSoup(html).findAll(text=True))
            self.pages[page] = message
        except urllib2.HTTPError as e:
            print e
    
        return message

    def raw_html(self, page):
        try:
            html = urllib2.urlopen(page).read()
        except urllib2.HTTPError as e:
            print e
    
        return html
        

    def params(self):
        return 0

#
