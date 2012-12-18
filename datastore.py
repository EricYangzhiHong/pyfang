#!/usr/bin/python
import md5

class Store:
    def __init__(self):

        # Page -> HTML
        self.pages = {}

        self.database_info = {}
        self.database = {}

        # Comparative Pre-computation stuff
        self.lookup_table = {}
        

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


    # Comparative Pre-computation stuff
    def create_lookup(self, values):
        """ Takes a dict of id, raw_html pairs and creates a lookup table using the
            md5 hash.
            :values:    Dict of strings. id => raw_html
        """

        self.lookup_table = {value: md5.new(values[value]).digest() for value in values}
        


