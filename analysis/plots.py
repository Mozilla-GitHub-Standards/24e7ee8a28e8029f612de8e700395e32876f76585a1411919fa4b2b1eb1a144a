# -*- coding: utf-8 -*-

import json
#import matplotlib as mp
import numpy as np
import matplotlib.pyplot as plt

#Imports a logfile and returns the array of JSON objects
def import_logfile(log_path):
    with open(log_path) as f:
        loglines = f.readlines()

    objects = []

    for i in range(len(loglines)):
        objects.append(json.loads(loglines[i]))
        
    return objects


#Prints shortsummary for each element in the dataset
def print_element_summary(objects):

    num_obj = len(objects)
    fails = 0

    print("\n")
    for i in range(num_obj):
        request_time = objects[i].get('response').get(
            'response_time') - objects[i].get('response').get('command_time')
        print("Host: ", objects[i].get('host'))
        print("Success: ", objects[i].get('success'))
        print("Rank: ", objects[i].get('rank'))
        print("Request time: ", request_time)
        signatureScheme = 'NA'
        if(objects[i].get('response').get(
                'result').get('info').get('ssl_status')):
            signatureScheme = objects[i].get('response').get(
                    'result').get('info').get('ssl_status').get(
                    'signatureSchemeName')
        print("Signature Scheme: ", signatureScheme)
        print("\n")
        if (objects[i].get('success') == False):
            fails += 1

    print('Total Objects: {}'.format(num_obj), 'Failed: ', fails)


#Plots response times vs. rank 
def plot_response_times(objects):

    num_obj = len(objects)
    fails = 0
    response_times = []
    ranks = []

    for i in range(num_obj):
        if (objects[i].get('success') == False):
            fails += 1
        else:
            request_time = objects[i].get('response').get(
                'response_time') - objects[i].get('response').get('command_time')
            response_times.append(request_time)
            ranks.append(objects[i].get('rank'))


    plt.scatter(ranks, response_times, marker=".")
    plt.show()

#Plots the number of successful/failed connections in a bar plot
def plot_success(objects):

    num_obj = len(objects)
    succ = 0
    fail = 0

    for i in range(num_obj):
        if(objects[i].get('success')):
            succ+=1
        else:
            fail+=1

    print('Total Objects: {}'.format(num_obj))
    print('Successful conncetions: {} of {}.   {} %'.format(succ, num_obj, succ/num_obj*100))
    plt.bar(['success','failure'], [succ,fail])
    plt.show()


#Prints overall statistics of the dataset.
def print_log_summary(objects):

    num_obj = len(objects)
    rqt_sum = 0
    
    for i in range(num_obj):
        request_time = objects[i].get('response').get(
                'response_time') - objects[i].get('response').get('command_time')
        rqt_sum += request_time
        
        
        
    rqt_avg = rqt_sum/num_obj
    print("Total Number of Elements: ", num_obj)
    print("Average Request time: ", rqt_avg)


def plot_CAs(objects, detailed):

    num_obj = len(objects)
    ca_list = {}
    
    for i in range(num_obj):
        try:
            IssuerName = objects[i].get('response').get('result').get(
                    'info').get('ssl_status').get('serverCert').get('issuer').get('commonName')
        except:
            IssuerName = "none"
        
        if (detailed):
            print("Host: ", objects[i].get('host'))
            print("Server Cert Issuer: ", IssuerName)
        if (IssuerName in ca_list):
            ca_list[IssuerName] += 1
        else:
            ca_list[IssuerName] = 1
        
    
    ca_names = ca_list.keys()
    for k in ca_names:
        print("Name: ", k, "  Number of Hosts: ", ca_list[k])