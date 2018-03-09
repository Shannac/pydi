import fnmatch
import os
import datetime
import csv
import requests
import base64
import math


# Returns a formatted authorization string to go into request header
def encode_credentials(client_id, client_secret):
    string_to_encode = client_id + ":" + client_secret
    encoded = base64.b64encode(string_to_encode.encode('ascii')).decode()
    credentials = "Basic " + encoded
    #print(credentials)
    return credentials


# Requests an access token and returns a formatted token string to go into request header
def get_token(api_key, credentials):
    url = "https://di-api.drillinginfo.com/v2/direct-access/tokens?grant_type=client_credentials"
    headers = {
        'x-api-key': api_key,
        'authorization': credentials,
        'content-type': "application/x-www-form-urlencoded"
        }
    response = requests.request("POST", url, headers=headers)
    token = response.json()['access_token']
    formatted_token = "Bearer " + token
    return formatted_token


# Constructs the request url based on the api version, the desired resource, and the request parameters (filters)
def format_url(api_version, data_service, list_of_filter_tuples):
    url = "https://di-api.drillinginfo.com/v" + str(api_version) + "/direct-access/"
    int_string = url + data_service + "?"
    index = 0
    for condition in list_of_filter_tuples:
        hold = str(condition[0]) + "=" + str(condition[1])
        if index <> len(list_of_filter_tuples)-1:
            int_string = int_string + hold + "&"
            index = index + 1
        else:
            int_string = int_string + hold
    formatted_url = int_string
    return formatted_url


# Sends a request to the version 1 api and returns a list of json objects, one for each page
def make_request_v1(formatted_url, api_key, page_start, page_end):
    output = []
    pages_requested = 1+page_end-page_start
    headers = {
        'x-api-key': api_key,
        'page': page_start,
        'cache-control': "no-cache",
        }
    print('Attempting request {} of {} ').format(page_start, pages_requested)
    try:
        response = requests.request("GET", formatted_url, headers=headers)
        response_json = response.json()
        output.append(response_json)
        records_available = int(response.headers['Content-Length'])
        pages_unrounded = records_available/100
        pages_available = int(math.ceil(pages_unrounded))
        #print('There are {} pages available').format(pages_available)
        page_number = page_start+1
        current_page = 2
        while page_number <= page_end:
                print('Attempting request {} of {} ').format(page_number, pages_requested)
                headers = {
                    'x-api-key': api_key,
                    'page': page_number,
                    'cache-control': "no-cache",
                }
                response = requests.request("GET", formatted_url, headers=headers)
                output.append(response.json())
                page_number = page_number + 1
                current_page = current_page + 1
    except(RuntimeError, TypeError):
        print("An error occurred requesting page {}; request number {} of {}").format(page_number, current_page, pages_requested)
    pages_received = current_page - 1
    print("{} pages successfully received.").format(pages_received)
    print('Process Finished')
    keys = sorted(response_json[0].keys())
    return output, pages_received, pages_available, keys


# Sends a request to the version 2 api and returns a single json object with the number of records specified in the header
def make_request_v2(formatted_url, api_key, formatted_token):
    headers = {
        'x-api-key': api_key,
        'cache-control': "no-cache",
        'authorization': formatted_token
    }
    try:
        response = requests.request("GET", formatted_url, headers=headers)
        response_json = response.json()
        record_count = len(response_json)
        keys = sorted(response_json[0].keys())
        print("{} records received.").format(record_count)
        print('Process Finished')
    except(RuntimeError, TypeError):
        print("An error occurred during the request: {}").format(response)
    return response_json, record_count, keys


### More consistent responses if the filters are passed as'parameters' to request() when using versin 2??
'''
def make_request_v2_2(api_key, formatted_token):
    url = "https://di-api.drillinginfo.com/v2/direct-access/producing-entities/"
    headers = {
        'x-api-key': api_key,
        'cache-control': "no-cache",
        'authorization': formatted_token,
    }
    params = {
        'state': 'TX',
        'prodtype': 'OIL',
    }
    response = requests.request("GET", url, headers=headers, params=params).json()
    #print(response)
    record_count = len(response)
    keys = sorted(response[0].keys())
    return response, record_count, keys
'''

# Append the records to a .csv file located in the root directory if there is one from the same day, else create a new one
def write_response(file_name, list_of_json_object):
    date_string = datetime.datetime.today().strftime('%Y-%m-%d')

    file_list = os.listdir('.')
    look_for = file_name+"_"+date_string+'.csv'
    output = []
    for entry in file_list:
        if fnmatch.fnmatch(entry, look_for):
            output.append(entry)

    if len(output) > 0:
        f = open(file_name + "_" + date_string + '.csv', 'a')
        writer = csv.writer(f)
        for record in list_of_json_object:
            writer.writerow(record.values())
        f.close()

    else:
        f = open(file_name + "_" + date_string + '.csv', 'w')
        writer = csv.writer(f)
        writer.writerow(list_of_json_object[0].keys())
        for record in list_of_json_object:
            writer.writerow(record.values())
        f.close()
