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

class CalcTestCase(unittest.TestCase):
    def setUp(self):
        #basedir = os.path.abspath(os.path.dirname(__file__))
        #app.config['TESTING'] = True
        #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        return self.app.post('/', follow_redirects=True)

    def input(self, entry):
        return self.app.post('/', data=dict(result=entry), follow_redirects=True)

    def test_simple_input(self):
         #enter the number
        rv = self.input('2+2')
        self.assertIn(b'4.0', rv.data)

    def test_bracket_input(self):
        rv = self.input('1+2*(123+23-123-2)-232-(322-23*38)')
        self.assertIn(b'363.0', rv.data)


if __name__ == '__main__':
    unittest.main()
