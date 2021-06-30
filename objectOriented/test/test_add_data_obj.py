import unittest
from unittest import mock
from add_data_obj import addData
import mysql.connector as mysql

class testAddData(unittest.TestCase):


    def test_DBConnect(self):
        class_inst = addData('tweets')
        actual_conn = class_inst.DBConnect()
        self.assertTrue(actual_conn)

if __name__ == '__main__':
    unittest.main()
