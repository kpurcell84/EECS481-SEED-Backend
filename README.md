EECS481-SEED-Backend
============
### Notes:
- SDK located in google_appengine directory
- hello-endpoints contains a hello world example for an endpoints API
- Each user consumes 672 GAE Ops per day to fetch data (30 min intervals)

#### To Run Locally:
- `google_appengine/dev_appserver.py seed-endpoints`
	- add option --clear_datastore=yes to clear local datastore
- Visit localhost:8000 for admin console
- Visit localhost:8080/_ah/api/explorer for API Explorer

#### To Package API:
- `google_appengine/endpointscfg.py get_client_lib java -bs gradle seed_api.SeedApi --application seed-endpoints/`

#### To Upload API:
- `google_appengine/appcfg.py update seed-endpoints/`
- Visit https://umichseed.appspot.com/_ah/api/explorer for API explorer

#### To Launch Remote API Shell:
- `PYTHONPATH=./seed-endpoints google_appengine/remote_api_shell.py -s umichseed.appspot.com`

### TODO:
- generate a representative data set
	- How to do this?

- google cloud messenger for notifications
	- Android client setup: https://github.com/GoogleCloudPlatform/gradle-appengine-templates/tree/master/GcmEndpoints
	- https://github.com/geeknam/python-gcm

- fill in time periods of no data with null for p_quant_data.get
	- do on client to minimize data passed over network

- Fix 500 char limit on watson q/a
	- must be truncated on front end

### API Calls:
