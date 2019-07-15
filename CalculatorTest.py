import unittest
import os
import json
from pythonCalc import app

#TEST_DB = 'test.db'

class BasicTestCase(unittest.TestCase):
    '''
    Testing that the calculator works as expected
    '''

    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    #no db to test yet, adding that functionality later
    #def test_database(self): #check that db exists
    #    tester = os.path.exists('calc.db')
    #    self.assertTrue(tester)

if __name__ == '__main__':
    unittest.main()
