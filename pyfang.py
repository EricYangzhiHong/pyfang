#!/usr/bin/python
"""
    Driver program for pyfang. Handles user-defined options and calls appropriate modules.

"""
import os, sys, urllib2
import pf_injection, pf_parser
import json

if __name__ == '__main__':

    page = sys.argv[1]

    mysql_params = ['database()', 'user()']

    data = pf_injection.injection(page, mysql_params)

    pf_parser.parse(data) 


