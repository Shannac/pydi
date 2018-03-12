# pydi

A Python API for accessing DrillingInfo


## Example Usage

Define your DrillingInfo credentials as operating system environment variables, e.g. in `bash` (**note:** these are not real keys)

```bash
export CLIENT_ID="12345-direct-access"
export CLIENT_SECRET="f8e3487f-9411-4297-bf98-b78bc0897ce5"
export API_KEY="facb5fdc082fef81598157a8b23992cg"
```

A simple Python script that gets 1000 producing entities from the state of Texas and the writes the results to a CSV file:

```python
import os
from pydi import PyDI

client_id = os.environ['CLIENT_ID']
client_secret = os.environ['CLIENT_SECRET']
api_key = os.environ['API_KEY']

di = PyDI(client_id, client_secret, api_key)

di.filter_records("producing-entities", [('State', 'TX'), ('pagesize', 1000)])
di.write_records("Producing-Entities_Texas")
```
