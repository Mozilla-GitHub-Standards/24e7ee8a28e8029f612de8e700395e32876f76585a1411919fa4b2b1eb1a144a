#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 17:56:50 2018

@author: jonasda
"""

import sqlite3
import json
import sys
import os

# Imports a logfile and the log metadata from a given folder.
# Returns the array of JSON objects and a single JSON object containing metadata.
def import_logfolder(log_path, **kwargs):
    
    with open(log_path+"/meta") as m:
        meta = json.loads(m.read())
    
    with open(log_path+"/log") as f:
        loglines = f.readlines()

    objects = []
    numlines = len(loglines)

    for i in range(numlines):
        objects.append(json.loads(loglines[i]))
        
    return objects, meta

try:
    source_folder = sys.argv[1]
except:
    print("Usage: Sepcify root directory.")
    exit

#source_folder = "/home/jonasda/WorkCanary/canary-harvester/client/data/"
#datetime = "2018-03-08Z00-05-24"

db_folder = source_folder + "database"

date_folders = os.listdir(source_folder)

if not os.path.exists(db_folder):
    os.makedirs(db_folder)

db = sqlite3.connect(db_folder + "/logs.db")

c = db.cursor()

for j in range(len(date_folders)):
    datetime = date_folders[j]
    data, meta = import_logfolder(source_folder + datetime)
    print("Processing " + datetime)
    
    #c.execute('''DROP TABLE IF EXISTS log''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS log ("id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "host" TEXT, "rank" INTEGER, "response_time" REAL, "success" TEXT,
                                                 "signature_scheme" TEXT, "error_class" TEXT, "raw_error" TEXT,
                                                 "CA_name" TEXT, "date" TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS testrun ("date" TEXT PRIMARY KEY, "max_timeout" INTEGER, "scans_per_host" INTEGER, "version" TEXT,
                                                 "build_ID" TEXT, "nspr_version" TEXT, "nss_version" TEXT,
                                                 "canary_version" TEXT)''')
    meta_date = meta['run_finish_time'][:10]
    meta_timeout = meta['args']['timeout']
    meta_scans = meta['args']['scans']
    meta_version = meta['test_metadata']['app_version']
    meta_build = meta['test_metadata']['application_ini']['buildid']
    meta_nspr = meta['test_metadata']['nspr_version']
    meta_nss = meta['test_metadata']['nss_version']
    meta_canary = meta['tlscanary_version']
    c.execute("INSERT INTO testrun VALUES ('{0}',{1},{2},'{3}','{4}','{5}','{6}','{7}')".format(meta_date, meta_timeout, 
                                          meta_scans, meta_version, meta_build, meta_nspr, meta_nss, meta_canary))
    
    for i in range(len(data)):
        response_time = data[i]['response']['response_time']
        command_time = data[i]['response']['command_time']
        request_time = response_time - command_time
        host = data[i]['host'].encode('UTF-8')
        rank = data[i]['rank']
        success = data[i]['success']
        try:
            signature_scheme = data[i]['response']['result']['info']['ssl_status']['signatureSchemeName'].encode('UTF-8')
        except:
            signature_scheme = 'NA'
        try:
            error_class = data[i]['response']['result']['info']['error_class'].encode('UTF-8')
        except:
            error_class = 'NA'
        try:
            raw_error = data[i]['response']['result']['info']['raw_error'].encode('UTF-8')
        except:
            raw_error = 'NA'
        try:
            CA_name = data[i]['response']['result']['info']['ssl_status']['serverCert']['issuer']['commonName'].replace("'", "").encode('UTF-8')
        except:
            CA_name = 'NA'
        date = meta['run_finish_time'][:10]   
        
        command = "INSERT INTO log ('host', 'rank', 'response_time', 'success', 'signature_scheme', \
                            'error_class', 'raw_error', 'CA_name', 'date') \
                            VALUES ('{0}',{1},{2},'{3}','{4}','{5}','{6}','{7}','{8}')".format(host, rank, 
                                          request_time, success, signature_scheme, error_class, raw_error, CA_name, date)
        #print(command)
        try:
            c.execute(command)
        except:
            print("Failed Command: ", command)
            
    db.commit()



