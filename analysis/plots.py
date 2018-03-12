# -*- coding: utf-8 -*-

import json
#import matplotlib as mp
#import numpy as np
import matplotlib.pyplot as plt

global ITEMLIMIT
ITEMLIMIT = 999999

# Imports a logfile and returns the array of JSON objects
def import_logfile(log_path, **kwargs):
    
    strip_certs = kwargs.get('strip_certs', None)
    
    with open(log_path) as f:
        loglines = f.readlines()

    objects = []

    for i in range(len(loglines)):
        objects.append(json.loads(loglines[i]))
        if(strip_certs):
            objects[i]['response']['result']['info']['certificate_chain'] = []
        
        
    return objects


# Imports a logfile and the log metadata from a given folder.
# Returns the array of JSON objects and a single JSON object containing metadata.
# Optionally removes certificate data from the objects to reduce memory usage.
def import_logfolder(log_path, **kwargs):
    
    strip_certs = kwargs.get('strip_certs', None)
    
    with open(log_path+"/meta") as m:
        meta = json.loads(m.read())
    
    with open(log_path+"/log") as f:
        loglines = f.readlines()

    objects = []

    for i in range(len(loglines)):
        objects.append(json.loads(loglines[i]))
        if(strip_certs):
            objects[i]['response']['result']['info']['certificate_chain'] = []
        
    return objects, meta


# Prints short summary for each element in the dataset
# Not recommended for large datasets.
def print_element_summary(objects):

    num_obj = len(objects)
    fails = 0

    print("\n")
    for i in range(num_obj):
        request_time = objects[i]['response'][
            'response_time'] - objects[i]['response']['command_time']
        print("Host: ", objects[i]['host'])
        print("Success: ", objects[i]['success'])
        print("Rank: ", objects[i]['rank'])
        print("Request time: ", request_time)
        signatureScheme = 'NA'
        if('ssl_status' in objects[i]['response'][
                'result']['info'].keys()):
            signatureScheme = objects[i]['response'][
                    'result']['info']['ssl_status']['signatureSchemeName']
        print("Signature Scheme: ", signatureScheme)
        print("\n")
        if (objects[i]['success'] == False):
            fails += 1

    print('Total Objects: {}'.format(num_obj), 'Failed: ', fails)


# Plots response times vs. rank 
def plot_response_times(objects, **kwargs):

    meta = kwargs.get('meta', None)
    
    num_obj = len(objects)
    fails = 0
    response_times = []
    ranks = []

    for i in range(num_obj):
        if (objects[i]['success'] == False):
            fails += 1
        else:
            request_time = objects[i]['response'][
                'response_time'] - objects[i]['response']['command_time']
            response_times.append(request_time)
            ranks.append(objects[i]['rank'])


    plt.scatter(ranks, response_times, marker=".")
    if meta:
        plt.title(meta['run_finish_time'][0:10])
    plt.show()


#Plots the number of successful/failed connections in a bar plot
def plot_success(objects, **kwargs):
    
    meta = kwargs.get('meta', None)

    num_obj = len(objects)
    succ = 0
    fail = 0

    for i in range(num_obj):
        if(objects[i]['success']):
            succ+=1
        else:
            fail+=1

    print('Total Objects: {}'.format(num_obj))
    print('Successful conncetions: {} of {}.   {} %'.format(succ, num_obj, succ/num_obj*100))
    plt.bar(['success','failure'], [succ,fail])
    if meta:
        plt.title(meta['run_finish_time'][0:10])
    plt.show()


#Prints overall statistics of the dataset.
def print_log_summary(objects, **kwargs):

    meta = kwargs.get('meta', None)
    
    num_obj = len(objects)
    rqt_sum = 0
    
    for i in range(num_obj):
        request_time = objects[i]['response'][
                'response_time'] - objects[i]['response']['command_time']
        rqt_sum += request_time
        
        
        
    rqt_avg = rqt_sum/num_obj
    if meta:
        print("Run date: ", meta['run_finish_time'][0:10])
    print("Total Number of Elements: ", num_obj)
    print("Average Request time: ", rqt_avg)


def plot_CAs(objects, **kwargs):
    
    detailed = kwargs.get('detailed', False)
    meta = kwargs.get('meta', None)
    
    if meta:
        print(meta['run_finish_time'][0:10])
        
    num_obj = len(objects)
    ca_list = {}
    
    for i in range(num_obj):
        try:
            IssuerName = objects[i]['response']['result'][
                    'info']['ssl_status']['serverCert']['issuer']['commonName']
        except:
            IssuerName = "none"
        
        if (detailed):
            print("Host: ", objects[i]['host'])
            print("Server Cert Issuer: ", IssuerName)
        if (IssuerName in ca_list):
            ca_list[IssuerName] += 1
        else:
            ca_list[IssuerName] = 1
        
    
    ca_names = sorted(ca_list, key=ca_list.get, reverse=True)
    for k in ca_names:
        print("Name: ", k, "\nNumber of Hosts: ", ca_list[k])


# Plots the response time difference for every host between two datasets. 
def compare_response_times(objects_a, objects_b, **kwargs):
    
    meta = kwargs.get('meta', None)
    
    num_obj_a = len(objects_a)
    num_obj_b = len(objects_b)
    
    host_list = {}
    
    rq_sum_a = 0
    rq_count_a = 0
    rq_sum_b = 0
    rq_count_b = 0
    rq_sum_diff = 0
    rq_count_diff = 0
    
    for i in range(min(max(num_obj_a, num_obj_b), ITEMLIMIT)):
        if(i < num_obj_a):
            host = objects_a[i]['host']
            request_time = objects_a[i]['response'][
                'response_time'] - objects_a[i]['response']['command_time']
            rq_count_a += 1
            rq_sum_a += request_time
            if (host in host_list):
                host_list[host]["time"] = host_list[host]["time"]-request_time
                host_list[host]["comp"] = True
                rq_sum_diff += host_list[host]["time"]
                rq_count_diff += 1
            else:
                host_list[host] = {"rank":objects_a[i]['rank'], "time":request_time, "comp":False}
                
        if(i < num_obj_b):
            host = objects_b[i]['host']
            request_time = objects_b[i]['response'][
                'response_time'] - objects_b[i]['response']['command_time']
            rq_count_b += 1
            rq_sum_b += request_time
            if (host in host_list):
                host_list[host]["time"] = request_time-host_list[host]["time"]
                host_list[host]["comp"] = True
                rq_sum_diff += host_list[host]["time"]
                rq_count_diff += 1
            else:
                host_list[host] = {"rank":objects_b[i]['rank'], "time":request_time, "comp":False}
    
    rq_avrg_a = rq_sum_a/rq_count_a
    rq_avrg_b = rq_sum_b/rq_count_b
    rq_avrg_diff = rq_sum_diff/rq_count_diff
    print("Averrage request time a: ", rq_avrg_a)
    print("Averrage request time b: ", rq_avrg_b)
    print("Averrage request time difference: ", rq_avrg_diff)

    
    ranks = []
    times = []    
    ranks2 = []
    times2 = []
    for key in host_list.keys():
        obj = host_list[key]
        if (obj["comp"] == True):
            ranks.append(obj["rank"])
            times.append(obj["time"])
        else:
            ranks2.append(obj["rank"])
            times2.append(obj["time"])
            
    plt.scatter(ranks, times, marker=".")
    plt.scatter(ranks2, times2, marker=".")
    if meta:
        plt.title(meta['run_finish_time'][0:10])
    plt.show()
    
    
# Compares connection failures between two datasets.
def compare_failures(objects_a, objects_b, **kwargs):
    
    meta = kwargs.get('meta', None)
    meta2 = kwargs.get('meta2', None)
    
    num_obj_a = len(objects_a)
    num_obj_b = len(objects_b)
    
    host_list = {}
    
    for i in range(min(max(num_obj_a, num_obj_b), ITEMLIMIT)):
        
        if(i < num_obj_a):
            host = objects_a[i]['host']
            success = objects_a[i]['success']
            if (host in host_list):
                host_list[host]["success_a"] = success
                host_list[host]["comp"] = True
            else:
                host_list[host] = {"rank":objects_a[i]['rank'], "success_a":success, "success_b":False, "comp":False}
                
        if(i < num_obj_b):
            host = objects_b[i]['host']
            success = objects_b[i]['success']
            if (host in host_list):
                host_list[host]["success_b"] = success
                host_list[host]["comp"] = True
            else:
                host_list[host] = {"rank":objects_b[i]['rank'], "success_a":False, "success_b":success, "comp":False}
    
    ranks = []
    compare_success = []
    succ = 0
    fail = 0
    new_succ = 0
    new_fail = 0
    for key in host_list.keys():
        obj = host_list[key]
        if (obj["comp"] == True):
            if(obj["success_a"] and obj["success_b"]):
                ranks.append(obj["rank"])
                compare_success.append(0)
                succ += 1
            if(not obj["success_a"] and obj["success_b"]):
                ranks.append(obj["rank"])
                compare_success.append(3)
                new_succ += 1
            if(obj["success_a"] and not obj["success_b"]):
                ranks.append(obj["rank"])
                compare_success.append(2)
                new_fail += 1
            if(not obj["success_a"] and not obj["success_b"]):
                ranks.append(obj["rank"])
                compare_success.append(1)
                fail += 1
    
    print("Summary: ", succ, " repeatedly successful.  ", new_succ, " newly successful.")
    print("         ", fail, " repeatedly failed.      ", new_fail, " newly failed.  ")
    plt.scatter(ranks, compare_success, marker=".")
    if (meta and meta2):
        plt.title(meta['run_finish_time'][0:10] + " vs. " + meta2['run_finish_time'][0:10])
    plt.show()


def list_error_codes(objects, **kwargs):
    
    meta = kwargs.get('meta', None)
    
    num_obj = len(objects)
    c = 0
    for i in range(num_obj):
        if (objects[i]['success'] == False):
            if (objects[i]['response']['result']['origin'] == "error_handler"):
                print("\n", objects[i])
                #print(i, " Host: ", objects[i]['host'])
                #print("Success: ", objects[i]['success'])
                #print("Rank: ", objects[i]['rank'])
                #print(objects[i]['response']['result']['info']['raw_error'])
            c +=1
        if (c > 25):
            break
            
