# Canary-Harvester

Canary-harvester was created to automatically collect general data about 
TLS-connections on the web by running daily 
[tls-canary](https://github.com/mozilla/tls-canary) scans on a set of
100.000 TLS-enabled websites. This data is stored in the Mozilla taskcluster 
environment and can be downloaded manually. 

This repository contains tools to facilitate downloading the data and converting
raw JSON-formatted logfiles into a handy sqlite-database.

**Disclaimer:** 

The tools are not paticularly user friendly, well tested, or well documented. 
Apologies for that. They were created to barely satisfy the project 
creators' needs and might be improved in the future.

## Client

The folder *client* contains the relevant tools for downloading the data from
taskcluster and creating the sqlite-database.

## All-In-One script

**data_collection.sh** combines all necessary steps to retrieve the canary log data 
from taskcluster and convert it to a sqlite-database. It can be restricted to 
a certain date range and it can also be used to update an already existing 
database if executed repeatedly in the same directory.
It keeps track of already downloaded artifacts and of data already written
to the database and skips unnecessary work accordingly.

Example:
```
.\data_collection.sh 2018-03-01 2018-03-15
```

### Requirements
Successful execution of the script **requires**:
- nodeJS (and the packages listed in package.json) 
- python 

to run the following independent subscripts.

### Subscripts

**main.js** uses the taskcluster api to compile a list of URLs, each representing 
the log artifact of a single canary-run. It takes start and end date as 
arguments to limit the list of URLs to a specific date range and returns a 
raw list of URLs. 

**database.py** parses raw logfiles from tls-canary scan runs and writes a small
selection of the included data to a sqlite-database for easier analysis and 
visualization. 

The script is optimized to process a folder structure as created
by data_collection.sh.

The default selection of information that is written to the database is based 
on the requirements of the creators of canary-havester, but different information
from the scans could be of interest for different users. Adapting the script 
accordingly is moderately complex.

### File Sizes

Download size of the compressed logfiles is around **45 Mb** per daily scan run. 

Extracted logfiles are significantly bigger, around **900 Mb** per scan run. 

The sqlite-Database grows by around **20 Mb** per added scan run. 
