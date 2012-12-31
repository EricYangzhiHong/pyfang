#!/usr/bin/python

class Reporter:

    def __init__(self):
        self.delimiter = '\t'
        
    def columns_in_statement(self, num_columns):
        print self.delimiter, 'Columns', self.delimiter, num_columns

    def magic_number(self, magic_num):
        print self.delimiter, 'Magic Number', self.delimiter, magic_num 

    def db_info(self, data):
        for key in data:
            print self.delimiter, key, self.delimiter, data[key]

    def tables(self, data):
        print 'Interesting tables:'
        for i in data:
            print self.delimiter, i

    def columns(self, columns):
        """
            :data: List of column names.
        """
        # Will need to be changed once funct is extended to work w/ multiple tables
        # data will probly be a Dict of Lists

        print self.delimiter, 'Columns:'
        for column in columns:
            print self.delimiter * 2, column

    def rows(self, rows):
        print self.delimiter * 2, 'Rows:'
        for row in rows:
            print self.delimiter * 3, row


