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
import random

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
    
if (source_folder[-1:] != "/"):
    source_folder += "/"

#source_folder = "/home/jonasda/WorkCanary/canary-harvester/client/data/"
#datetime = "2018-03-08Z00-05-24"

db_folder = source_folder + "database"

log_folders = os.listdir(source_folder)

random.seed()

if not os.path.exists(db_folder):
    os.makedirs(db_folder)

open(db_folder + "/history", 'a').close()

db = sqlite3.connect(db_folder + "/logs.db")

c = db.cursor()

for j in range(len(log_folders)):
    datetime = log_folders[j]
    
    
    
    with open(db_folder + "/history", 'r') as hist:
        if (datetime in hist.read()):
            print("Skipping " + datetime + ". Already in database.")
            continue

    with open(db_folder + "/history", 'a') as hist:
            hist.write(datetime + "\r\n")
    
    print("Reading " + datetime + "...")
    try:
        data, meta = import_logfolder(source_folder + datetime)
    except:
        print("Skipping " + datetime)
        continue

    
    print("Writing " + datetime + " to DB...")
    
    c.execute('''CREATE TABLE IF NOT EXISTS log ("id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,"run_id" INTEGER, "host" TEXT, "rank" INTEGER, "response_time" REAL, "connect_success" TEXT,
                                                 "command_success" TEXT, "signature_scheme" TEXT, "cipher_name" TEXT, "protocol_version" TEXT, "cert_untrusted" TEXT, "error_class" TEXT, 
                                                 "raw_error" TEXT, "short_error" TEXT, "CA_name" TEXT, "date" TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS testrun ("run_id" INTEGER PRIMARY KEY NOT NULL, "date" TEXT, "max_timeout" INTEGER, "scans_per_host" INTEGER, "version" TEXT,
                                                 "build_ID" TEXT, "nspr_version" TEXT, "nss_version" TEXT,
                                                 "canary_version" TEXT)''')
    
    unique = False
    while (not unique):
        run_id = random.randint(100000, 999999)
        unique = not (run_id,) in c.execute('''SELECT run_id FROM testrun''')
    
    meta_date = meta['run_finish_time'][:10]
    meta_timeout = meta['args']['timeout']
    meta_scans = meta['args']['scans']
    meta_version = meta['test_metadata']['app_version']
    meta_build = meta['test_metadata']['application_ini']['buildid']
    meta_nspr = meta['test_metadata']['nspr_version']
    meta_nss = meta['test_metadata']['nss_version']
    meta_canary = meta['tlscanary_version']
    c.execute("INSERT INTO testrun VALUES ({0},'{1}',{2},{3},'{4}','{5}','{6}','{7}', '{8}')".format(run_id, meta_date, meta_timeout, 
                                          meta_scans, meta_version, meta_build, meta_nspr, meta_nss, meta_canary))
    
    for i in range(len(data)):
        response_time = data[i]['response']['response_time']
        command_time = data[i]['response']['command_time']
        request_time = response_time - command_time
        host = data[i]['host'].encode('UTF-8')
        rank = data[i]['rank']
        command_success = data[i]['success']
        connection_success = data[i]['response']['success']
        try:
            signature_scheme = data[i]['response']['result']['info']['ssl_status']['signatureSchemeName'].encode('UTF-8')
        except:
            signature_scheme = 'NA'
        try:
            cipher_name = data[i]['response']['result']['info']['ssl_status']['cipherName'].encode('UTF-8')
        except:
            cipher_name = 'NA'
        try:
            protocol_version = data[i]['response']['result']['info']['ssl_status']['protocolVersion']
        except:
            protocol_version = 'NA'
        try:
            cert_untrusted = data[i]['response']['result']['info']['ssl_status']['isUntrusted']
        except:
            cert_untrusted = 'NA'
        try:
            error_class = data[i]['response']['result']['info']['error_class']
        except:
            error_class = 'NA'
        try:
            raw_error = data[i]['response']['result']['info']['raw_error'].encode('UTF-8')
        except:
            raw_error = 'NA'
        try:
            short_error = data[i]['response']['result']['info']['short_error_message'].encode('UTF-8')
        except:
            short_error = 'NA'
        try:
            CA_name = data[i]['response']['result']['info']['ssl_status']['serverCert']['issuerCommonName'].replace("'", "").encode('UTF-8')
        except:
            CA_name = 'NA'
        date = meta['run_finish_time'][:10]   
        
        command = "INSERT INTO log ('run_id', 'host', 'rank', 'response_time', 'connect_success', 'command_success', 'signature_scheme', 'cipher_name', 'protocol_version', \
                            'cert_untrusted', 'error_class', 'raw_error','short_error', 'CA_name', 'date') \
                            VALUES ({0},'{1}',{2},{3},'{4}','{5}','{6}','{7}','{8}', '{9}', '{10}', '{11}', '{12}','{13}', '{14}')".format(run_id, host, rank, 
                                          request_time, connection_success, command_success, signature_scheme, cipher_name, protocol_version, cert_untrusted, error_class,
                                          raw_error, short_error, CA_name, date)

        try:
            c.execute(command)
        except:
            print("Failed Command: ", command)
            
    db.commit()



