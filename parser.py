#!/usr/bin/python
import re


def most_common(l):
    """ Helper function. 
        :l: List of strings.
        :returns: most common string.
    """
    # another way to get max of list?
    #from collections import Counter
    #data = Counter(your_list_in_here)
    #data.most_common()   # Returns all unique items and their counts
    #data.most_common(1)

    count = 0
    answer = ''

    for element in l:
        if l.count(element) > count:
            count = l.count(element)
            answer = element 

    return answer 

class Parser:
    """ Parses data gleaned from injections, prints them and stores them in a datastore."""

    def __init__(self, store):
        """ Create Lists of keywords for tables and columns.
            :store:     Store object, holds dicts of DB information and tables.
        """
        self.store = store
        self.table_keywords = ['user', 'usr', 'password', 'pass', 'pwd']
        self.column_keywords = ['user', 'usr', 'password', 'pass', 'pwd']
        self.exclude = set(open('./lists/mysql/excluded_tables').readlines())

    def html_diff(self, pre, post):
        """ Diffs two strings of HTML by splitting on whitespace.
            :pre:       HTML without SQLI
            :post:      HTML with SQLI
            :returns:   List of strings. Difference between two URL's HTML.
        """
        return list(set(post.split()) - set(pre.split()))

        """
        for word in pre:
            if word in post:
                post.remove(word)
        return post
        """

    def params(self, data):
        """ Parses HTML for DB info.
            :data:      Dict of lists.
            :returns:   Dict of lists.
        """

        values = {}
        for key in data:
            candidates = []

            for value in data[key]:

                token = value.replace('"','').replace("'",'')
                if '=' in token:
                    token = re.sub('.*=','',token)
                token = re.sub('<.*>','', token)
                candidates.append(token)

            values[key] = most_common(candidates)
        # maybe? #max(number_counts.iteritems(), key = operator.itemgetter(1))[0]

        self.store.db_values(values)
        return values    

    def tables(self, data):
        """ Gets tables of interest from raw data.
                Heuristic currently checks for possibly interesting values like 'user'.
            :data:      Dict of Lists, currently only Dict entry is 'table_name'
            :returns:   List of strings. Tables with interesting names.
        """
        
        values = []
        for datum in data:
            for table in data[datum]:
                if any(i in str(table).lower() for i in self.table_keywords):
                    values.append(str(table))

        # Exclude common config tables by default
        values = list(set(values) - self.exclude)

        self.store.tables(values)
        return values 

    def columns(self, tables):
        """ Finds columns of interest.
                Heuristic currently checks for possibly interesting values like 'user'.
                Also should exclude common config MySQL tables.
            :data:      Dict of lists. Table->Columns
            :returns:   List of strings. Columns. 
        """
        values = {}

        for table in tables:
            columns = tables[table]
            values[table] = []

            for column in columns:
                if any(i in str(column).lower() for i in self.column_keywords):
                    values[table].append((str(column)))

        self.store.columns(columns)
        return values

    def rows(self, data):
        """ Takes column data for each column for a table
            :data: Dict of Lists
            :returns:
        """

        return 0

