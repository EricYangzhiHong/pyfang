import unittest
import sys, os
import pyfang 
import builder, datastore, injector, scanner, obfuscator, parser, reporter

class Test_fang(unittest.TestCase):
    """
    A test class for the fang module.
    """
    # Create major classes
    def setUp(self):
        print 'Setting up tests...'
        print 'Setup done.\n'

    def test_get_visible_nums(self):
        scan = scanner.Scanner()
        store = datastore.Store()
        parse = parser.Parser(store)

        print 'Testing parser\'s get visible params method...'

        # CTF6 from LAMPSec
        pre = scan.page('http://192.168.83.134/index.php?id=null')
        post = scan.page('http://192.168.83.134/index.php?id=null%20UNION%20SELECT%201,2,3,4,5,6,7')
        for i in parse.get_visible_nums(parse.html_diff(pre, post)):
            self.assertTrue(i.isdigit())

        # PenTesterLab
        pre = scan.page('http://192.168.83.130/cat.php?id=null')
        post = scan.page('http://192.168.83.130/cat.php?id=null%20UNION%20SELECT%201,%202,%203,4')
        for i in parse.get_visible_nums(parse.html_diff(pre, post)):
            self.assertTrue(i.isdigit())
        print 'Test done.\n'

    def test_get_num_columns(self):
        print 'okay'






    """
    # Tests using VMWare basic SQLi from pentesterlabs
    def test_injection(self):
        print 'Testing basic injection with VMWare from pentesterlabs.com...'

        # IP is from my VM, vulnerable page and param already known.
        page = 'http://192.168.83.130/cat.php?id=1' 
        mysql_params = ['database()', 'user()']
        print injection.injection(page, mysql_params)
        print 'Basic injection done.'
    """

if __name__ == '__main__':
    unittest.main()


