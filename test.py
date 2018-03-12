#!/usr/bin/env python

#A quick example of how to:
#
# get five pages of permit records (100 per page) in Reeves Co and write the results to a .csv file in the directory
# containing the pydi.py file
#
# get the first 1000 producing entities in Texas and write the results to a .csv file in the directory containing
# the pydi.py file

import unittest
import os

from pydi import PyDI

class TestPyDI(unittest.TestCase):

    def setUp(self):
        self.client_id = os.environ['CLIENT_ID']
        self.client_secret = os.environ['CLIENT_SECRET']
        self.api_key = os.environ['API_KEY']
        self.di = PyDI(self.client_id, self.client_secret, self.api_key)

    def test_encode_creditials(self):

        credentials = self.di.encode_credentials(self.client_id, self.client_secret)

        self.assertEqual(credentials, os.environ['CREDS'])

    def test_get_token_returns_string(self):

        credentials = self.di.encode_credentials(self.client_id, self.client_secret)
        token = self.di.get_token(credentials)

        self.assertTrue(isinstance(token, str))

    def test_format_url(self):

        formatted_url = self.di.format_url("producing-entities", [('State', 'TX'), ('pagesize', 1000)])

        self.assertEqual(formatted_url, 'https://di-api.drillinginfo.com/v2/direct-access/producing-entities?State=TX&pagesize=1000')


    def test_filter_records_length(self):

        self.di.filter_records("producing-entities", [('State', 'TX'), ('pagesize', 1000)])

        self.assertEqual(len(self.di.filtered_records), 1000)


    def test_filter_records_query(self):

        self.di.filter_records("producing-entities", [('State', 'TX'), ('pagesize', 1000)])

        for item in self.di.filtered_records:
            if item['CurrOperId'] == 100358928:
                assert item['CurrOperNo'] == '073056'



if __name__ == '__main__':
    unittest.main()
