#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 12:09:40 2018

@author: jonasda
"""
from plots import plot_response_times, plot_success, print_log_summary, print_element_summary, plot_CAs, import_logfile


data = import_logfile("/home/jonasda/WorkCanary/Data/2018-02-08-09-41-16/log")
#data2 = import_logfile("/home/jonasda/WorkCanary/Data/2018-02-06Z16-55-12/log")


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