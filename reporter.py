#!/usr/bin/python

class Reporter:

    def __init__(self):
        self.delimiter = '\t'
        
    def columns_in_statement(self, num_columns):
        print 'Columns', self.delimiter, num_columns

    def db_info(self, data):
        for key in data:
            print key, self.delimiter, data[key]


