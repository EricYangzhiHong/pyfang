import unittest
import sys, os
# Add to path variable and import to test
sys.path.append('../')
import fang 

class Test_fang(unittest.TestCase):
    """
    A test class for the fang module.
    """
    # Create major classes
    def setUp(self):
        print 'Creating fang...'
        self.fang = fang.fang() 

        print 'Setup done.'

if __name__ == '__main__':
    unittest.main()

