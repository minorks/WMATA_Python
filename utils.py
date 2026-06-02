# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 21:36:59 2026

@author: hokie
"""

import pandas as pd

def getData(file):
    dat = pd.read_csv(file,parse_dates=['StartTime','Sched_Arr','Time'])
    dat['DOW'] = dat['StartTime'].dt.day_name()
    
    for x in ['StartTime','Sched_Arr','Time']:
        dat[x] = dat[x].dt.tz_convert("America/New_York")
    
    # TODO: Want the MAX time for all stop_sequence indices except the 
    # MAX index where we want the MIN time.
    dat = dat.groupby(['Trip_ID','DOW','stop_name','StartTime','direction_id'])\
         .agg({'Time':"min"})
    return(dat.reset_index())
