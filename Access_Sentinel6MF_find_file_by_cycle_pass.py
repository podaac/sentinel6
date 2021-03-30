#!/usr/bin/env python3

# # Access Sentinel-6 MF Data using a script
# This script shows a simple way to maintain a local time series of Sentinel-6  data using the [CMR Search API](https://cmr.earthdata.nasa.gov/search/site/docs/search/api.html). It downloads granules the ingested since the previous run to a designated data folder and overwrites a hidden file inside with the timestamp of the CMR Search request on success.
# Before you beginning this tutorial, make sure you have an Earthdata account: [https://urs.earthdata.nasa.gov] .
# Accounts are free to create and take just a moment to set up.



####
#Users are encouraged to use data files from March 11th 2021 onwards.
####

import urllib
from urllib import request
from http.cookiejar import CookieJar
import getpass
import netrc
import requests
import json
import socket 
###############The lines below are to get the IP address. You can make this static and assign a fixed value to the IPAddr variable
hostname = socket.gethostname()    
IPAddr = socket.gethostbyname(hostname)
######################################

print("Running Sentinel-6 MF Data Download")

# ## Before you start
# 
# Before you beginning this tutorial, make sure you have an Earthdata account: [https://urs.earthdata.nasa.gov].
# 
# Accounts are free to create and take just a moment to set up.
# 
# ## Authentication setup
# 
# The function below will allow Python scripts to log into any Earthdata Login application programmatically.  To avoid being prompted for
# credentials every time you run and also allow clients such as curl to log in, you can add the following
# to a `.netrc` (`_netrc` on Windows) file in your home directory:
# 
# ```
# machine urs.earthdata.nasa.gov
#     login <your username>
#     password <your password>
# ```
# 
# Make sure that this file is only readable by the current user or you will receive an error stating
# "netrc access too permissive."
# 
# `$ chmod 0600 ~/.netrc` 
# 
# *You'll need to authenticate using the netrc method when running from command line with [`papermill`](https://papermill.readthedocs.io/en/latest/). You can log in manually by executing the cell below when running in the notebook client in your browser.*


def setup_earthdata_login_auth(endpoint):
    """
    Set up the request library so that it authenticates against the given Earthdata Login
    endpoint and is able to track cookies between requests.  This looks in the .netrc file 
    first and if no credentials are found, it prompts for them.

    Valid endpoints include:
        urs.earthdata.nasa.gov - Earthdata Login production
    """
    try:
        username, _, password = netrc.netrc().authenticators(endpoint)
    except (FileNotFoundError, TypeError):
        # FileNotFound = There's no .netrc file
        # TypeError = The endpoint isn't in the netrc file, causing the above to try unpacking None
        print("There's no .netrc file or the The endpoint isn't in the netrc file")

    manager = request.HTTPPasswordMgrWithDefaultRealm()
    manager.add_password(None, endpoint, username, password)
    auth = request.HTTPBasicAuthHandler(manager)

    jar = CookieJar()
    processor = request.HTTPCookieProcessor(jar)
    opener = request.build_opener(auth, processor)
    request.install_opener(opener)

###############################################################################
# GET TOKEN FROM CMR 
###############################################################################
def get_token( url: str,client_id: str, user_ip: str,endpoint: str) -> str:
    try:
        token: str = ''
        username, _, password = netrc.netrc().authenticators(endpoint)
        xml: str = """<?xml version='1.0' encoding='utf-8'?>
        <token><username>{}</username><password>{}</password><client_id>{}</client_id>
        <user_ip_address>{}</user_ip_address></token>""".format(username, password, client_id, user_ip)
        headers: Dict = {'Content-Type': 'application/xml','Accept': 'application/json'}
        resp = requests.post(url, headers=headers, data=xml)
        response_content: Dict = json.loads(resp.content)
        token = response_content['token']['id']
    except:
        print("Error getting the token - check user name and password")
    return token
###############################################################################
# DELETE TOKEN FROM CMR 
###############################################################################
def delete_token(url: str, token: str) -> None:
	try:
		headers: Dict = {'Content-Type': 'application/xml','Accept': 'application/json'}
		url = '{}/{}'.format(url, token)
		resp = requests.request('DELETE', url, headers=headers)
		if resp.status_code == 204:
			print("CMR token successfully deleted")
		else:
			print("CMR token deleting failed.")
	except:
		print("Error deleting the token")
	exit(0)
###############################################################################
# Downloading the file
###############################################################################

# The script uses the CMR API to get files by API see https://cmr.earthdata.nasa.gov/search/site/docs/search/api.html#g-cycle - Get data by cycle 
# https://cmr.earthdata.nasa.gov/search/site/docs/search/api.html#g-passes - Get data by cycle 
# Code below is a very simplistic version of getting data for one cycle and pass

edl="urs.earthdata.nasa.gov"
cmr="cmr.earthdata.nasa.gov" 

setup_earthdata_login_auth(edl)
token_url="https://"+cmr+"/legacy-services/rest/tokens"
token=get_token(token_url,'Sentinel-6', IPAddr,edl)


 
Short_Name="SHORTNAME OF THE PRODUCT TO DOWNLOAD"
#This is the Short Name of the product you want to download 
# See Finding_shortname.pdf file

### Download Files only with the following extensions
## Sentinel-6 MF datasets also have *.bufr.bin, *.DBL, *.rnx, *.dat 
extensions = ['.nc','.bin']

data = "DOWNLOAD LOCATION" 
#You should change `data` to a suitable download path on your file system. 



from os import makedirs
import datetime
from os.path import isdir, basename
from urllib.parse import urlencode
from urllib.request import urlopen, urlretrieve
from datetime import datetime, timedelta
from json import dumps, loads


# **The search retrieves granules for a particular cycle and pass. 
# Pass is an optional parameter -- If pass is not provided then all files for a particular pass will be used

### Define the cycle and pass you need in this section
s6mf_cycle=2
s6mf_pass=245

params = {
    'scroll': "true",
    'page_size': 2000,
    'sort_key': "-start_date",
    'ShortName': Short_Name, 
    'cycle[]':s6mf_cycle ,
    'passes[0][pass]':s6mf_pass,
     'token': token
}



# Get the query parameters as a string and then the complete search url:

query = urlencode(params)
url = "https://"+cmr+"/search/granules.umm_json?"+query
print(url)


# Get a new timestamp that represents the UTC time of the search. Then download the records in `umm_json` format for granules that match our search parameters:


with urlopen(url) as f:
    results = loads(f.read().decode())

print(str(results['hits'])+" granules available for Cycle:"+str(s6mf_cycle)+" and Pass:"+str(s6mf_pass))


# Neatly print the first granule record (if one was returned):

if len(results['items'])>0:
    print(dumps(results['items'][0], indent=2))


# The link for http access can be retrieved from each granule record's `RelatedUrls` field. 
# The download link is identified by `"Type": "GET DATA"` but there are other data files in EXTENDED METADATA" field.
# Select the download URL for each of the granule records:


downloads_all=[]
downloads_data = [[u['URL'] for u in r['umm']['RelatedUrls'] if u['Type']=="GET DATA" and ('Subtype' not in u or u['Subtype'] != "OPENDAP DATA")] for r in results['items']]
downloads_metadata = [[u['URL'] for u in r['umm']['RelatedUrls'] if u['Type']=="EXTENDED METADATA"] for r in results['items']]

for f in downloads_data: downloads_all.append(f)
for f in downloads_metadata: downloads_all.append(f)

downloads = [item for sublist in downloads_all for item in sublist]

# Finish by downloading the files to the data directory in a loop. 
success_cnt=failure_cnt=0

for f in downloads:
    try:
        for extension in extensions:
            if f.lower().endswith((extension)):
                urlretrieve(f, data+"/"+basename(f))
                print(datetime.now())
                print("SUCCESS: "+f+"\n\n")
                success_cnt=success_cnt+1
    except Exception as e:
        print(datetime.now())
        print("FAILURE: "+f+"\n\n")
        failure_cnt=failure_cnt+1
        print(e)


print("Downloaded: "+str(success_cnt)+" files\n")
print("Files Failed to download:"+str(failure_cnt)+"\n")
delete_token(token_url,token) 
print("END \n\n")



