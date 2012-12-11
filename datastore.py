#!/usr/bin/python

class Store:
    def __init__(self):
        self.database_info = {}
        self.database = {}

    def db_values(self, values):
        self.database_info = values

    def tables(self, values):
        """ Takes a Dict of Lists. Keys are table names, values are table columns
            Turns this into a Dict of Dicts of Lists.
        """
        self.database = values

    def columns(self, values):
        return 0

    def rows(self, values):
        return 0


