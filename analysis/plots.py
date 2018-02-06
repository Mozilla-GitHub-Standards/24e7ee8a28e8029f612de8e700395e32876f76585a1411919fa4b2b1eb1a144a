# -*- coding: utf-8 -*-

import json
#import matplotlib as mp
import numpy as np
import matplotlib.pyplot as plt



def print_element_summary(log_path):
    with open(log_path) as f:
        loglines = f.readlines()

    objects = []

    for i in range(len(loglines)):
        objects.append(json.loads(loglines[i]))

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
        print("Signature Scheme: ",objects[i].get('response').get(
                'result').get('info').get('ssl_status').get(
                        'signatureSchemeName'))
        print("\n")
        if (objects[i].get('success') == False):
            fails += 1

    print('Total Objects: {}'.format(num_obj), 'Failed: ', fails)



def plot_response_times(log_path):
    with open(log_path) as f:
        loglines = f.readlines()

    objects = []

    for i in range(len(loglines)):
        objects.append(json.loads(loglines[i]))

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


    plt.scatter(ranks, response_times)
    plt.show()


def plot_success(log_path):
    with open(log_path) as f:
        loglines = f.readlines()

    objects = []

    for i in range(len(loglines)):
        objects.append(json.loads(loglines[i]))

    num_obj = len(objects)
    succ = 0
    fail = 0

    for i in range(num_obj):
        if(objects[i].get('success')):
            succ+=1
        else:
            fail+=1

    print('Total Objects: {}'.format(num_obj))
    plt.bar(['success','failure'], [succ,fail])
    plt.show()

def print_log_summary(log_path):
    with open(log_path) as f:
        loglines = f.readlines()

    objects = []

    for i in range(len(loglines)):
        objects.append(json.loads(loglines[i]))

    num_obj = len(objects)
    rqt_sum = 0
    
    for i in range(num_obj):
        request_time = objects[i].get('response').get(
                'response_time') - objects[i].get('response').get('command_time')
        rqt_sum += request_time
        
        
        
    rqt_avg = rqt_sum/num_obj
    print("Total Number of Elements: ", num_obj)
    print("Average Request time: ", rqt_avg)
        
logfile = "/home/jonasda/WorkCanary/Data/2018-02-06Z14-50-28/log"
logfile = "/home/jonasda/.tlscanary/log/2018/01/2018-01-25Z11-41-32/log"
print_element_summary(logfile)
#plot_response_times(logfile)
#plot_success(logfile)
print_log_summary(logfile)

