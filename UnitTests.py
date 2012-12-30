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


    def test_get_num_columns(self):
        print '1st test.'
        print 'Getting number of columns for building UNION statements...'

        # CTF6 from LAMPSec
        page = self.CTF6_page
        real_num_cols = 7
        num_cols_found = pyfang.num_columns(page, True)
        self.assertTrue(num_cols_found == real_num_cols)

        # PenTesterLab
        page = self.PTL_page
        real_num_cols = 4
        num_cols_found = pyfang.num_columns(page, True)
        self.assertTrue(num_cols_found == real_num_cols)

        print 'Test done.\n'

    def test_get_visible_nums(self):
        print '2nd test.'
        print 'Getting visible numbers on page using UNION SELECT sqli...'

        # CTF6 from LAMPSec
        page = self.CTF6_page
        num_cols = pyfang.num_columns(page, False)
        for i in pyfang.visible_nums(page, num_cols, True):
            self.assertTrue(i.isdigit())

        # PenTesterLab
        page = self.PTL_page
        num_cols = pyfang.num_columns(page, False)
        for i in pyfang.visible_nums(page, num_cols, True):
            self.assertTrue(i.isdigit())

        print 'Test done.\n'


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


