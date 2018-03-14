#!/usr/bin/env python
# Copyright 2018 Erick Meany, John T. Foster

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

   # http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import unittest
import os

from pydi import PyDI

class TestPyDI(unittest.TestCase):

    def setUp(self):
        self.client_id = os.environ['CLIENT_ID']
        self.client_secret = os.environ['CLIENT_SECRET']
        self.api_key = os.environ['API_KEY']
        self.di = PyDI(self.client_id, self.client_secret, self.api_key)

    def test_encode_creditials_returns_string(self):

        credentials = self.di.encode_credentials(self.client_id, self.client_secret)

        self.assertTrue(isinstance(credentials, str))

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
