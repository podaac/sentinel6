# Scripted Access to PODAAC Sentinel 6 datasets

![N|Solid](https://podaac.jpl.nasa.gov/sites/default/files/image/custom_thumbs/podaac_logo.png)

The example script is provided for one dataset. 
  - These scripts can be set up as a cron that runs every hour or set up to download data per user needs
  - PO.DAAC is providing this script as “starter” script for download -- advanced features can be added and it would be great if you can contribute these code back to PO.DAAC.
  - The search and download relies on an API as defined at https://cmr.earthdata.nasa.gov/search/site/docs/search/api.html

## Step 1:  Get Earthdata Login     

https://urs.earthdata.nasa.gov/ 
> The Earthdata Login provides a single mechanism for user registration and profile  management for all EOSDIS system components (DAACs, Tools, Services). Your Earthdata login   also helps the EOSDIS program better understand the usage of EOSDIS services to improve  user experience through customization of tools and improvement of services. EOSDIS data are  openly available to all and free of charge except where governed by international  agreements.

## Step 2: Create a Manifest file
Contents of the file is as follows
```
<token>
  <username>YOUR URS USERID </username>
  <password> YOUR URS PASSWORD </password>
  <client_id>S6_test</client_id>
  <user_ip_address>YOUR IP ADDRESS</user_ip_address>
</token>
 ```
Save this file as mytokengenerator.xml

## Step 3: Get Token  
```
curl -X POST --header "Content-Type: application/xml" -d @mytokengenerator.xml https://cmr.earthdata.nasa.gov/legacy-services/rest/tokens
```

## Step 4:  Save the token information from the return
The return will be something like this.
```
<?xml version="1.0" encoding="UTF-8"?>
<token>
  <id>YOUR TOKEN WILL BE HERE</id>
  <username>YOUR URS USERID</username>
  <client_id>S6 TEST</client_id>
  <user_ip_address>YOUR IP ADDRESS</user_ip_address>
</token>
```

## Step 5:  Update Script 
 Update script to identify the shortname for which the data needs to be downloaded. Also, provide a storage location. Provide absolute paths and not relative paths to the storage location. 
 
Example below 
```
Short_Name="JASON_CS_S6A_L1B_GNSS_POD_DAILY"
data = "/tmp" 
bounding_extent="-180,-90,180,90" 
```
## Note 1: Downloading All or specific files for a collection 
The code is meant to be generic – for some data products, there is more than one file that can be a data files.
To get just the raw data file as defined by the metadata swap out
```
downloads_metadata = [[u['URL'] for u in r['umm']['RelatedUrls'] if u['Type']=="EXTENDED METADATA"] for r in results['items']] 
```
to 
```
downloads_metadata = []
```
## Note 2: Download files with specific extensions 
```
downloads = [item for sublist in downloads_all for item in sublist]
filter_files = ['.nc', '.dat','.bin']  # This will only download netcdf, data, and binary files, you can add/remove other data types as you see fit
import re
def Filter(list1, list2):
    return [n for n in list1 if
             any(m in n for m in list2)]
downloads=Filter(downloads,filter_files)
```
### In need of Help?
The PO.DAAC User Services Office is the primary point of contact for answering your questions concerning data and information held by the PO.DAAC. User Services staff members are knowledgeable about both the data ordering system and the data products themselves. We answer questions about data, route requests to other DAACs, and direct questions we cannot answer to the appropriate information source. 

Please contact us via email at podaac@podaac.jpl.nasa.gov 



