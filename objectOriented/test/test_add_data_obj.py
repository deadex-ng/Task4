import unittest
from unittest import mock
from add_data_obj import addData
import mysql.connector as mysql

class testAddData(unittest.TestCase):


    def test_DBConnect(self):
        expected_conn = mysql.connect(host='localhost', user='user', password='user',
                             database='tweets', buffered=True)
        class_inst = addData('tweets')
        actual_conn = class_inst.DBConnect()
        self.assertEqual(expected_conn,actual_conn)

if __name__ == '__main__':
    unittest.main()
