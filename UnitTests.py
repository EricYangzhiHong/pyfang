import unittest
import sys, os
import pyfang 
import pf_injection

class Test_fang(unittest.TestCase):
    """
    A test class for the fang module.
    """
    # Create major classes
    def setUp(self):
        print 'Setting up tests...'
        print 'Setup done.'

    # Tests using VMWare basic SQLi from pentesterlabs
    def test_injection(self):
        print 'Testing basic injection with VMWare from pentesterlabs.com...'

        # IP is from my VM, vulnerable page and param already known.
        page = 'http://192.168.83.130/cat.php?id=1' 
        mysql_params = ['database()', 'user()']
        print pf_injection.injection(page, mysql_params)

        print 'Basic injection done.'

if __name__ == '__main__':
    unittest.main()


