#!/usr/bin/python
import re

def most_common(l):
    """ Takes list of strings.
        Returns most common string.
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


