# -*- coding: utf-8 -*-
"""
Created on Mon May 11 20:38:14 2026

@author: hokie
"""

class Trip:
    runs = dict()
    def __init__(self,tid,route,tdir,dow):
        self.id = tid
        self.dir = tdir
        self.dow = dow
        self.route = route

class Stop:
    def __init__(self,sid,name):
        self.id = sid
        self.name = name
        
class Route:
    stops = list()
    def __init__(self,rAb,rName):
        self.abb = rAb
        self.name = rName
    
    def addStop(self,toAdd):
        self.stops.append(toAdd)
        
        
def setStaticData(direct):
    
    # Create Routes
    routes = set()
    f = open(direct+"/routes.txt","r")
    f.seek(1)
    for line in f:
        temp = line.split(",")
        routes.add(Route(temp[0],temp[3]))
    f.close()
    
    # Create Stops
    stops = set()
    f = open(direct+"/stops.txt","r")
    for line in f:
        temp = line.split(",")
        stops.add(Stop(temp[0],temp[2]))
    f.close()
        
    return([routes,stops])
