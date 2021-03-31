#!/usr/bin/env python3


# This script shows a simple way to create a subset of Sentinel-6 MF data using Harmony API.
## Access Sentinel-6 MF Data using Harmony API
## https://harmony.earthdata.nasa.gov/ 
## Python module for Harmony API can be installed from https://github.com/nasa/harmony


#Other modules needed
#pip3 install helper
#pip3 install progressbar
#pip3 install python-dotenv


import helper
import netrc
import datetime as dt
from harmony import BBox, Client, Collection, Request


###################
def harmony_client_login_auth(endpoint):
    """
    Set up the request library so that it authenticates against the given Earthdata Login
    endpoint.  This looks in the .netrc file first and if no credentials are found, it prompts for them.

    Valid endpoints include:
        urs.earthdata.nasa.gov - Earthdata Login production
    """
    try:
        username, _, password = netrc.netrc().authenticators(endpoint)
    except (FileNotFoundError, TypeError):
        # FileNotFound = There's no .netrc file
        # TypeError = The endpoint isn't in the netrc file, causing the above to try unpacking None
        print("There's no .netrc file or the The endpoint isn't in the netrc file")
    return Client(auth=(username, password))
###################
edl="urs.earthdata.nasa.gov"
collection = Collection(id='C1238543220-POCLOUD')

harmony_client=harmony_client_login_auth(edl)

request = Request(
    collection=collection,
    spatial=BBox(-10, -10, 10, 10)
)

job1_id = harmony_client.submit(request)
print(harmony_client.status(job1_id))
print(harmony_client.result_json(job1_id, show_progress=False))

futures = harmony_client.download_all(job1_id)
for f in futures:
    print(f.result())