#!/usr/bin/env python

#A quick example of how to:
#
# get five pages of permit records (100 per page) in Reeves Co and write the results to a .csv file in the directory
# containing the pydi.py file
#
# get the first 1000 producing entities in Texas and write the results to a .csv file in the directory containing
# the pydi.py file

import unittest

from pydi import PyDI

class TestPyDI(unittest.TestCase):

    def setUp(self):
        self.client_id = "12976-direct-access"
        self.client_secret = "b8e7487e-9411-4177-be96-e98ec7877be4"
        self.api_key = "facb5adc983fed80599157a8a33972cf"
        self.di = PyDI(self.client_id, self.client_secret, self.api_key)

    def test_encode_creditials(self):

        credentials = self.di.encode_credentials(self.client_id, self.client_secret)

        self.assertEqual(credentials, 'Basic MTI5NzYtZGlyZWN0LWFjY2VzczpiOGU3NDg3ZS05NDExLTQxNzctYmU5Ni1lOThlYzc4NzdiZTQ=')

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
