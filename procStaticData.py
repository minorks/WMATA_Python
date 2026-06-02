# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 21:09:00 2026

@author: hokie
"""
import pandas as pd

folder = "M:\\Python\\WMATA_Py\\Unzipped\\"

def setStaticData():
    # 'Routes' assigns a route_id to its long and short names
    routes = pd.read_csv(folder+"routes.txt",usecols=[0,2,3])
    
    # 'Calendar' associates a SERVICE_ID with one or more {Days of the week} 
    # on which the service is valid.
    cal = pd.read_csv(folder+"calendar.txt",dtype={'route_id' : 'str',
            'monday':'bool', 'tuesday':'bool','wednesday':'bool',
            'thursday':'bool','friday':'bool',
            'saturday':'bool','sunday':'bool'},
                      date_format={'start_date':'%Y%M%D','end_date':'%Y%M%D'})
    
    # 'Trips' alignes ROUTES with SERVICE_ID (day(s) of week) and DIRECTION
    # Columns selected are route_id,service_id,trip_id,trip_headsign,direction
    trips = pd.read_csv(folder+"trips.txt",usecols=[0,1,2,3,4])
    
    # 'Stop_Times' aligns each TRIP_ID with a sequenced set 
    sTimes = pd.read_csv(folder+"stop_times.txt",usecols=['trip_id','stop_id',
                                    'arrival_time','stop_sequence','timepoint'])
    
    # 'Stops' aligns stop IDs with (text) names
    stops = pd.read_csv(folder+"stops.txt",usecols=['stop_id','stop_name'])
    
    sched = trips.merge(routes,on='route_id',how='left').\
        merge(cal,on='service_id',how='left').\
            merge(sTimes,on='trip_id',how='right').\
                merge(stops,on='stop_id',how='inner').\
                    sort_values(by=['trip_id','direction_id','stop_sequence'])
                    
    return(sched)

def makeSchedFiles(sched,routes=None):
    fLoc = "M:\\Python\\WMATA_Py\\Schedules\\"
    rts = sched['route_id'].unique() if routes==None else routes
    for rt in rts:
        sched[sched['route_id']==rt].to_csv(fLoc+rt+".csv")