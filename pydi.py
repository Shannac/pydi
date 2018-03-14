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
import fnmatch
import os
import datetime
import csv
import requests
import base64
import math


class PyDI(object):

    """Class that instantiates an object that can be used to query the DrillingInfo (DI) database.

    Args: 
        client_id (str): The DI customer client id.
        client_secret (str): The DI customer client secret
        api_key (str): The DI customer API key

    Attributes:
        api_version (str): The DI API version, default value is 2.
        token (str): DI token that is returned from login at class instantiation
    """

    def __init__(self, client_id, client_secret, api_key):

        self.api_key = api_key

        self.api_version = "2"
        self.root_url = "https://di-api.drillinginfo.com/v" + self.api_version

        credentials = self.encode_credentials(client_id, client_secret)
        
        self.token = self.get_token(credentials) 

        self.headers = {
            'x-api-key': self.api_key,
            'cache-control': "no-cache",
            'authorization': self.token
        }


    def encode_credentials(self, client_id, client_secret):
        """Creates a formatted authorization string to go into request header

        Args: 
            client_id (str): The DI customer client id.
            client_secret (str): The DI customer client secret

        Returns:
            (str): A string of the form 'Basic x6oaslxbh00...'

        """
        string_to_encode = client_id + ":" + client_secret
        encoded = base64.b64encode(string_to_encode.encode('ascii')).decode()
        return  "Basic " + encoded


    def get_token(self, credentials):
        """Requests an access token and creates a formatted token string to go into request header

        Args: 
            credentials (str): The DI credential string returned from successful login

        Returns:
            (str): A one time use token for DI API access.
  
        """
        url = self.root_url + "/direct-access/tokens?grant_type=client_credentials"
        headers = {
            'x-api-key': self.api_key,
            'authorization': credentials,
            'content-type': "application/x-www-form-urlencoded"
            }
        response = requests.request("POST", url, headers=headers)
        token = response.json()['access_token']
        return "Bearer " + token


    def format_url(self, data_service, list_of_filter_tuples):
        """ 
            Constructs the request url based the desired resource, and the request parameters (filters)
        """
        url = self.root_url + "/direct-access/"
        int_string = url + data_service + "?"
        index = 0
        for condition in list_of_filter_tuples:
            hold = str(condition[0]) + "=" + str(condition[1])
            #What is this?
            if index < len(list_of_filter_tuples)-1:
                int_string = int_string + hold + "&"
                index = index + 1
            else:
                int_string = int_string + hold

        return int_string

    def filter_records(self, data_service, list_of_filter_tuples):
        """
            Sends a request to api and returns a single json object with the number of records specified in the header
        """
        try:
            formatted_url = self.format_url(data_service, list_of_filter_tuples)
            response = requests.get(formatted_url, headers=self.headers)
            response_json = response.json()
            record_count = len(response_json)
            self.filtered_records = response_json
        except(RuntimeError, TypeError):
            print('An error occurred during the filtering request')



### More consistent responses if the filters are passed as'parameters' to request() when using versin 2??
# '''
# def make_request_v2_2(api_key, formatted_token):
    # url = "https://di-api.drillinginfo.com/v2/direct-access/producing-entities/"
    # headers = {
        # 'x-api-key': api_key,
        # 'cache-control': "no-cache",
        # 'authorization': formatted_token,
    # }
    # params = {
        # 'state': 'TX',
        # 'prodtype': 'OIL',
    # }
    # response = requests.request("GET", url, headers=headers, params=params).json()
    # #print(response)
    # record_count = len(response)
    # keys = sorted(response[0].keys())
    # return response, record_count, keys
# '''

    def write_records(self, file_basename):
        """
            Append the records to a .csv file located in the root directory if there is one from the same day, otherwise create a new one
        """

        date_string = datetime.datetime.today().strftime('%Y-%m-%d')

        file_list = os.listdir('.')
        look_for = file_basename + "_" + date_string + '.csv'
        output = []
        for entry in file_list:
            if fnmatch.fnmatch(entry, look_for):
                output.append(entry)
            if len(output) > 0:
                with open(file_basename + "_" + date_string + '.csv', 'a') as f:
                    writer = csv.writer(f)
                    for record in self.filter_records:
                        writer.writerow(record.values())
            else:
                with open(file_basename + "_" + date_string + '.csv', 'w') as f:
                    writer = csv.writer(f)
                    writer.writerow(self.filtered_records[0].keys())
                    for record in self.filtered_records:
                        writer.writerow(record.values())
