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
            :store: Store object, holds dicts of DB information and tables.
        """
        self.store = store
        self.table_keywords = ['user', 'usr', 'password', 'pass', 'pwd']
        self.column_keywords = ['user', 'usr', 'password', 'pass', 'pwd']

    def html_diff(self, before_injection, after_injection):
        """ Diffs two lits of HTML.
            :before_injection: HTML without SQLI
            :after_injection: HTML with SQLI
            :returns: list of strings representing difference (hopefully captures SQLI info)
        """
        return list(set(after_injection) - set(before_injection))

    def db_values(self, data):
        """ Parses HTML for DB info.
            :data: Dict of lists.
            :returns: Dict of parsed lists.
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

    def information_schema(self, data):
        """ Get tables of interest.
                Heuristic currently checks for possibly interesting values like 'user'.
                Also should exclude common config MySQL tables.
            :data:
            :returns: Dict of list of parsed tables.
        """
        # Currently only queries on table_name
        values = [str(table) for table in data['table_name'] if 'user' in str(table).lower()]

        self.store.tables(values)
        return values 

    def table_for_columns(self, data):
        """ Takes table_names. Parses to get tables of interest.
                Heuristic currently checks for possibly interesting values like 'user'.
                Also should exclude common config MySQL tables.
            :returns: List of columns.
        """
        # in future, should store dict of lists like this for tables other than just 'users'.
        values = []

        for column in data['users']:
            if any(i in str(column).lower() for i in self.column_keywords):
                values.append(str(column))

        self.store.columns(values)
        return values 

    def columns_for_rows(self, data):
        """ Takes column data for each column for a table
            :data: Dict of Lists
            :returns:
        """

        return 0





