# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import json
#import matplotlib as mp
import numpy as np
import matplotlib.pyplot as plt


def plot_response_times(log_path, detailed):
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
        request_time = objects[i].get('response').get('response_time') - objects[i].get('response').get('command_time')
        if(detailed):
            print("Host: ",objects[i].get('host'))
            print("Success: ", objects[i].get('success'))
            print("Rank: ", objects[i].get('rank'))
            print("Request time: ", request_time)
        response_times.append(request_time)
        ranks.append(objects[i].get('rank'))
        if (objects[i].get('success') == False):
            fails += 1
    
    print ('Total Objects: {}'.format(num_obj), 'Failed: ', fails)
    
    plt.scatter(ranks, response_times)
    #plt.show()

def plot_success(log_path, detailed):
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
        request_time = objects[i].get('response').get('response_time') - objects[i].get('response').get('command_time')
        if(detailed):
            print("Host: ",objects[i].get('host'))
            print("Success: ", objects[i].get('success'))
            print("Rank: ", objects[i].get('rank'))
            print("Request time: ", request_time)
        response_times.append(request_time)
        ranks.append(objects[i].get('rank'))
        if (objects[i].get('success') == False):
            fails += 1
    
    print ('Total Objects: {}'.format(num_obj), 'Failed: ', fails)
    
    plt.scatter(ranks, response_times)
    
    

plot_response_times("/home/jonasda/.tlscanary/log/2018/01/2018-01-25Z11-26-24/log", False)
plot_response_times("/home/jonasda/.tlscanary/log/2018/01/2018-01-25Z11-41-32/log", False)

plt.show