'''

A quick example of how to:

    get five pages of permit records (100 per page) in Reeves Co and write the results to a .csv file in the directory
    containing the pydi.py file

    get the first 1000 producing entities in Texas and write the results to a .csv file in the directory containing
    the pydi.py file

'''

import pydi
import datetime

api_key = "facb5adc983fed80599157a8a33972cf"
client_id = "12976-direct-access"
client_secret = "b8e7487e-9411-4177-be96-e98ec7877be4"

# using di api version 1
# requesting permits
date_string = datetime.datetime.today().strftime('%Y-%m-%d')
data_service = "permits"
filters = [('state_province', 'Texas'), ('county_parish', 'Reeves'), ('min_expired_date', date_string)]
formatted_url = pydi.format_url(1, data_service, filters)
permits = pydi.make_request_v1(formatted_url, api_key, 1, 5)  # (first pate to get, last page to get))
for page in range(0, len(permits[0][:])):
    pydi.write_response("Permits_Reeves", permits[0][page])


# using di api version 2
# requesting producing entities
date_string_2 = "gt(" + datetime.datetime.today().strftime('%Y') + ")"
data_service = "producing-entities"
filters = [('State', 'TX'), ('pagesize', 1000)]
formatted_url = pydi.format_url(2, data_service, filters)
credentials = pydi.encode_credentials(client_id, client_secret)
formatted_token = pydi.get_token(api_key, credentials)
producing_entities = pydi.make_request_v2(formatted_url, api_key, formatted_token)
pydi.write_response("Producing-Entities_Texas", producing_entities[0])
