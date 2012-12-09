#!/usr/bin/python
"""
    Driver program for pyfang. Handles user-defined options and calls appropriate modules.

    OPTIONS to support:
        -f:     \n-delimited text file of parameters to inject (default is mysql_params).
        -d:     Delimiter to use. Default is '/**/', also can use:
                                             '%20' 
        -db:    Database to try injections against (default is MySQL). Only MySQL supported as of now.
        -v:     Verbose mode.
"""

import os, sys, urllib2
import builder, injection, parser, reporter
import json

if __name__ == '__main__':

    if len(sys.argv) == 1:
        print 'Help?'
        sys.exit(0)

    page = sys.argv[1]

    # Dicts of useful params for various DBs. 
    # Turn into text files so user can use their own.
    mysql_params = ['database()', 'user()', '@@version', '@@datadir', '@@hostname']

    inject = injection.Injector("")
    report = reporter.Reporter()
    parse = parser.Parser()
    #print b.build_union_injection(4,2)
    #print results['database()']


    """ 0) Find vuln. param
        1) union select to get num cols
        3) Get DB, user, version, etc
        4) get table list, print interesting table names
        5) select int. tables, get col # and names
        6) grab selected col. info
    """
    
    # Get number of columns
    #num_columns = inject.get_num_columns(page) 
    #report.columns_in_statement(num_columns)
    print inject.get_visible_param(page)
    # Get data
    #data = inject.injection(page, mysql_params) 
    #report.db_info(parse.db_values(data))


