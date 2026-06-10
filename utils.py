# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 21:36:59 2026

@author: hokie
"""

import pandas as pd
from time import sleep,ctime
import controller
import sys

# =============================================================================
# def getData(file):
#     dat = pd.read_csv(file,parse_dates=['StartTime','Sched_Arr','Time'])
#     dat['DOW'] = dat['StartTime'].dt.day_name()
#     
#     for x in ['StartTime','Sched_Arr','Time']:
#         dat[x] = dat[x].dt.tz_convert("America/New_York")
#     
#     # TODO: Want the MAX time for all stop_sequence indices except the 
#     # MAX index where we want the MIN time.
#     dat = dat.groupby(['Trip_ID','DOW','stop_name','StartTime','direction_id'])\
#          .agg({'Time':"min"})
#     return(dat.reset_index())
# =============================================================================

def runner(fLoc,secs=14400,routes=["F28","F29"]):
    x = 0
    
    # Blank Dictionary
    dats = {}
    for rt in routes:
        dats[rt] = controller.makeDataframe(feed=None)
    
    # Check every 10 seconds for 4 hours (4hrs*60mins*60secs = 14400)
    while x < secs:
        data = controller.retrieveBuffer()
        for rt,tbl in dats.items():
            tbl = pd.concat([tbl,controller.makeDataframe(feed=data,routes=[rt])])
        x += 10
        if x < secs:
            sleep(10)
            
    for rt,tbl in dats.items():
        tbl = tbl.groupby(by=['Trip_ID','Route','Stop_ID'],as_index=False)\
            ['ArrTime'].max().sort_values(by=['Trip_ID','ArrTime'])
        tbl.to_csv(fLoc+rt+"_data.csv",mode='a',index=False,header=False)
        print("Wrote to "+floc+rt+"_data.csv")

    print(ctime() + ": Ended WMATA Data Collection"
        
# runner(fLoc="/home/minorks/Python/WMATA_Py/Data/",secs=10)

if __name__ == "__main__":
    print(ctime() + ": Starting WMATA Data Collection"
    if (len(sys.argv) == 2):
        fLoc = str(sys.argv[1])
        runner(fLoc)
    elif (len(sys.argv) == 3):
        fLoc = str(sys.argv[1])
        secs = int(sys.argv[2])
        runner(fLoc,secs)
    elif (len(sys.argv) > 3):
        fLoc = str(sys.argv[1])
        secs = int(sys.argv[2])
        routes = []
        for i in range(3,len(sys.argv)):
          routes.append(str(sys.argv[i]))
        runner(fLoc,secs,routes)
    else:
        print("Error: Must Declare a File Location!")
        

