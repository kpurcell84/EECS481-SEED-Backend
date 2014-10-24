EECS481-SEED-Backend
============
### Notes:
- SDK located in google_appengine directory
- hello-endpoints contains a hello world example for an endpoints API

#### To Run Locally:
- `google_appengine/dev_appserver.py seed-endpoints`
	- add option --clear_datastore=yes to clear local datastore
- Visit localhost:8000 for admin console
- Visit localhost:8080/_ah/api/explorer for API Explorer

#### To Package API:
- `google_appengine/endpointscfg.py get_client_lib java -bs gradle seed_api.SeedApi --application seed-endpoints/`

### TODO:
- finalize schema
- generate a representative data set
- google cloud messenger for notifications

### API Calls:
- doctor getting all patients data