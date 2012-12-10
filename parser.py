#!/usr/bin/python
import re

def most_common(l):
    """ Helper function. Takes list of strings.
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
    """ Parses data gleaned from injections, prints them and stores them in a datastore.
        :store: Store object, holds dicts of DB information and tables.
    """
    def __init__(self, store):
        self.store = store

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
        """ Takes dict of list of table_names. Parses to get tables of interest.
                Heuristic currently checks for possibly interesting values like 'user'.
                Also should exclude common config MySQL tables.
            :returns: Dict of list of parsed tables.
        """
        
        values = {}
        
        # Currently only queries on table_name
        values = [str(table) for table in data['table_name'] if 'user' in str(table).lower()]

        self.store.table_names(values)
        return values 

    def table(self, data):
        """ Takes dict of list of table_names. Parses to get tables of interest.
                Heuristic currently checks for possibly interesting values like 'user'.
                Also should exclude common config MySQL tables.
            :returns: Dict of list of parsed tables.
        """
        
        values = {}
        
        # Currently only queries on table_name
        values = [str(table) for table in data['users'] if 'user' in str(table).lower()]

        self.store.table_names(values)
        return values 


