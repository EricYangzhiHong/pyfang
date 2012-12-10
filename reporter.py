#!/usr/bin/python

class Reporter:

    def __init__(self):
        self.delimiter = '\t'
        
    def columns_in_statement(self, num_columns):
        print self.delimiter, 'Columns', self.delimiter, num_columns

    def db_info(self, data):
        for key in data:
            print self.delimiter, key, self.delimiter, data[key]

    def tables(self, data):
        for i in data:
            print self.delimiter, i

    def columns(self, data):
        # Will need to be changed once funct is extended to work w/ multiple tables
        # data will probly be a Dict of Lists
        print self.delimiter, 'Table:', 'users'
        print self.delimiter, 'Columns:'

        for i in data:
            print self.delimiter * 2, i
