#!/usr/bin/python
import re

def most_common(l):
    """ Takes list of strings.
        :returns: most common string.
    """

    count = 0
    answer = ''

    for element in l:
        if l.count(element) > count:
            count = l.count(element)
            answer = element 

    return answer 

class Parser:
    """ Parses data gleaned from injections.

    """
    def __init__(self):
        self.x = 0

    def db_values(self, data):
        """ Takes dictionary with lists.
            keys are injected SQL strings.
            values are data leaked from injection.
            returns dictionary of parsed lists (hopefully answers)
        """

        answers = {}
        for key in data:
            candidates = []

            for value in data[key]:

                token = value.replace('"','').replace("'",'')
                if '=' in token:
                    token = re.sub('.*=','',token)
                token = re.sub('<.*>','', token)
                candidates.append(token)

            answers[key] = most_common(candidates)
        # maybe? #max(number_counts.iteritems(), key = operator.itemgetter(1))[0]

        return answers    

# another way to get max of list?
#from collections import Counter
#data = Counter(your_list_in_here)
#data.most_common()   # Returns all unique items and their counts
#data.most_common(1)

    def information_schema(self, data):
        """ Takes dict of list of table_names. Parses to get tables of interest.
            Heuristic currently checks for possibly interesting values like 'user'.
            Also should exclude common config MySQL tables.
            :returns: list of parsed tables.
        """
        
        # Currently only queries on table_name
        return [table for table in data['table_name'] if 'user' in str(table).lower()]



