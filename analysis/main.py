#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 12:09:40 2018

@author: jonasda
"""
from plots import plot_response_times, plot_success, print_log_summary, print_element_summary, plot_CAs, import_logfile, compare_response_times, compare_failures


#
#data = import_logfile("/home/jonasda/WorkCanary/canary-harvester/client/data/2018-02-08Z11-22-37/log", False)

#data2 = import_logfile("/home/jonasda/WorkCanary/canary-harvester/client/data/2018-02-09Z00-01-22/log", False)

#data3 = import_logfile("/home/jonasda/WorkCanary/canary-harvester/client/data/2018-02-10Z00-03-33/log")

#data4 = import_logfile("/home/jonasda/WorkCanary/canary-harvester/client/data/2018-02-11Z00-01-18/log")

data = import_logfile("/home/jonasda/WorkCanary/canary-harvester/client/data/2018-02-12Z00-01-50/log", True)

data2 = import_logfile("/home/jonasda/WorkCanary/canary-harvester/client/data/2018-02-13Z00-01-43/log", True)

#data2= import_logfile("/home/jonasda/WorkCanary/Data/2018-02-06Z16-55-12/log")


# =============================================================================
# 
# #print_element_summary(logfile)
# plot_response_times(data)
# plot_response_times(data2)
# #plot_success(logfile)
# #print_log_summary(logfile)
# print_log_summary(data2)
# =============================================================================

plot_response_times(data)
plot_response_times(data2)
plot_success(data)
plot_success(data2)
print_log_summary(data)
print_log_summary(data2)
plot_CAs(data, False)
plot_CAs(data2, False)
compare_response_times(data, data2)
compare_failures(data, data2)