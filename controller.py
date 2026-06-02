# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 12:50:10 2026

@author: hokie
"""
from google.transit import gtfs_realtime_pb2 as pb
import requests
import pandas as pd

key = "822c300f00bc4bb2a1781728dd7a659a"
tUp = "https://api.wmata.com/gtfs/bus-gtfsrt-tripupdates.pb"
myRoutes = ["F28","F29"]

def retrieveBuffer():
    headers = {
        "api_key": f"{key}", # Format may vary per API
        }
    resp = requests.get(tUp,headers=headers)
    
    feed = pb.FeedMessage()
    feed.ParseFromString(resp.content)
    return feed

def makeDataframe(feed, routes= None):
    df = pd.DataFrame({
        "AsOf" : pd.Series('datatime64[ns]'),
        "Trip_ID" : pd.Series(dtype='int'),
        "Route" : pd.Series(dtype='str'),
        #"StartTime" : pd.Series(dtype='datetime64[s]'),
        "Stop_ID" : pd.Series(dtype='int'),
        "ArrTime" : pd.Series(dtype='datetime64[s]')
        })
    
    asof = pd.to_datetime(feed.header.timestamp,utc=True,unit="s").\
        tz_convert("America/New_York")
    for msg in feed.entity:
        trip = {"trip" : msg.trip_update.trip,
                "stu" : msg.trip_update.stop_time_update}

        rt = trip["trip"].route_id
        
        if not (routes is None) and not (rt in routes):
            continue
        
        tid = trip["trip"].trip_id
        # sTime = my_datetime(trip["trip"].start_time).\
        # sTime = pd.to_datetime(trip["trip"].start_time,utc=True,unit="s").tz_convert("America/New_York")
        sid = trip["stu"][0].stop_id
        
        val = trip["stu"][0].departure.time if trip["stu"][0].HasField("departure")\
            else trip["stu"][0].arrival.time
        time = pd.to_datetime(val,utc=True,unit="s").\
            tz_convert("America/New_York")
        #df.loc[len(df)] = [asof,tid,rt,sTime,sid,time]
        df.loc[len(df)] = [asof,tid,rt,sid,time]

    return df

def my_datetime(date):
    if (date[0:2]=="24"):
        return pd.to_datetime(date.replace("24","00",1),utc=True,unit="s") +\
            pd.Timedelta(days=1)
    else:
        return pd.to_datetime(date,utc=True,unit="s")
 
# Debugging   
data = retrieveBuffer()
tbl = makeDataframe(data)
