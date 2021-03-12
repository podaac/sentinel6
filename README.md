# Scripted Access to PODAAC Sentinel 6-MF datasets

![N|Solid](https://podaac.jpl.nasa.gov/sites/default/files/image/custom_thumbs/podaac_logo.png)

The example script is provided for one dataset. 
  - These scripts can be set up as a cron that runs every hour or set up to download data per user needs
  - PO.DAAC is providing this script as “starter” script for download -- advanced features can be added and it would be great if you can contribute these code back to PO.DAAC.
  - The search and download relies on an API as defined at https://cmr.earthdata.nasa.gov/search/site/docs/search/api.html

## Step 1:  Get Earthdata Login     
This step is needed only if you dont have an Earthdata login already.
https://urs.earthdata.nasa.gov/ 
> The Earthdata Login provides a single mechanism for user registration and profile  management for all EOSDIS system components (DAACs, Tools, Services). Your Earthdata login   also helps the EOSDIS program better understand the usage of EOSDIS services to improve  user experience through customization of tools and improvement of services. EOSDIS data are  openly available to all and free of charge except where governed by international  agreements.



## Step 2:  Update Script  -- Get data by time and spatial bounds
This is applicable for file **Access_Sentinel6MF_usingshortname.py**

Update script to identify the shortname, file extenstions and spatial region for which the data needs to be downloaded. Also, provide a storage location. Provide absolute paths and not relative paths to the storage location. 
 
Example below 
```
Short_Name="JASON_CS_S6A_L1B_GNSS_POD_DAILY"
data = "/tmp" 
bounding_extent="-180,-90,180,90" 
extensions = ['.nc','.bin']

## Step 2:  Update Script  -- Get data by Pass/Cycle
This  is applicable for file **Access_Sentinel6MF_find_file_by_cycle_pass.py**

The search retrieves granules for a particular cycle and pass. Pass is an optional parameter -- If pass is not provided then all files for a particular pass will be used
Define the cycle and pass you need in this section. 
 
Example below 
```
s6mf_cycle=2
s6mf_pass=245
```

## Note 1: netrc file 
The netrc used within the script  will allow Python scripts to log into any Earthdata Login without being prompted for
credentials every time you run. The netrc file should be placed in your HOME directory.
To find the location of your HOME directory 

On UNIX you can use 
```
echo $HOME 
```
On Windows you can use 
```
echo %HOMEDRIVE%%HOMEPATH%
```

The output location from the command above should be the location of the `.netrc` (`_netrc` on Windows) file. 

**If the script cannot find the netrc file, you will be prompted to enter the username and passowrd and the script wont be able to generate the CMR token**



## Note 2: Downloading all or specific files for a collection 
The code is meant to be generic – for some data products, there is more than one file that can be a data files.
To get just the raw data file as defined by the metadata swap out
```
downloads_metadata = [[u['URL'] for u in r['umm']['RelatedUrls'] if u['Type']=="EXTENDED METADATA"] for r in results['items']] 
```
to 
```
downloads_metadata = []
```
## Note 3: Download files with specific extensions 
```
downloads = [item for sublist in downloads_all for item in sublist]
filter_files = ['.nc', '.dat','.bin']  # This will only download netcdf, data, and binary files, you can add/remove other data types as you see fit
import re
def Filter(list1, list2):
    return [n for n in list1 if
             any(m in n for m in list2)]
downloads=Filter(downloads,filter_files)
```

## Note 4: Pre-generate tokens
The example code manages CMR tokens internally for access to data. The tokens can be pre-generated using the information provided in [a Token Generation](Get_API_Token.pdf)


## Note 5: Create static IP address 
IP Address information is needed for CMR token generation. If the system running the code has a static IP address (or IP address that doesnt change too often), then you can hard-code the IP address in the IPAddr variable. This can speed up the script and optimize performance. 

```
hostname = socket.gethostname()    
IPAddr = socket.gethostbyname(hostname)
```

### In need of Help?
The PO.DAAC User Services Office is the primary point of contact for answering your questions concerning data and information held by the PO.DAAC. User Services staff members are knowledgeable about both the data ordering system and the data products themselves. We answer questions about data, route requests to other DAACs, and direct questions we cannot answer to the appropriate information source. 

Please contact us via email at podaac@podaac.jpl.nasa.gov 



