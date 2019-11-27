from django.shortcuts import render
from pg import DB
from django.http import HttpResponse, JsonResponse
import re
import time

# Create your views here.

db = DB(dbname='jabra', host='127.0.0.1', port=5432, user="", passwd="")
def home(request):
    global db
    q = db.query("SELECT * FROM TELEMETRY;")
    rooms_list = []
    rooms = []
    for i in q:
        room = i[0]
        if room not in rooms_list:
            peoplecount, inuse, timestamp = getPeopleCountAndUsage(room)
            rooms.append((room, peoplecount, inuse))
            rooms_list.append(room)
            print(rooms)
        else:
            continue
    return render(request, 'home.html', {'rooms':rooms, 'roomslist': rooms_list})


def room_stats(request, room):
    global db
    q = db.query("SELECT peoplecount, zones FROM TELEMETRY WHERE timestamp_=(SELECT MAX(timestamp_) FROM TELEMETRY WHERE roomid='%s');" % room)
    for i in q:
        peoplecount = i[0]
        zones = i[1]
    print(zones)
    return render(request, 'room_stats.html', {'current_pc': peoplecount, 'room': room, 'zones': zones})


def getPeopleCountAndUsage(room):
    global db 
    print(room)
    q = db.query("SELECT peoplecount, busystatus, timestamp_ FROM TELEMETRY WHERE timestamp_=(SELECT MAX(timestamp_) FROM TELEMETRY WHERE roomid='%s') AND roomid='%s';" % (room, room))
    if q:
        for i in q:
            peoplecount = i[0]
            inuse = i[1]
            timestamp = i[2]
    else:
        peoplecount = 0
        inuse = 0
        timestamp = 0
    return peoplecount, inuse, timestamp
    

def getPeopleCountAverage(room):
    global db
    q = db.query("SELECT AVG(peoplecount) FROM TELEMETRY WHERE roomid='%s';" % room)
    return q
        
    
def refreshRoomStats(request):
    global db
    room = request.META['QUERY_STRING']
    q = db.query("SELECT peoplecount, busystatus, zones, timestamp_ FROM TELEMETRY WHERE timestamp_=(SELECT MAX(timestamp_) FROM TELEMETRY WHERE roomid='%s');" % room)
    for i in q:
        peoplecount = i[0]
        busystatus = i[1]
        zones = i[2]
        timestamp = i[3]
        if time.time() - timestamp > 60:
            active = 0
        else:
            active = 1
    data = {'current_pc': peoplecount, 'streaming': busystatus, 'zones' : zones, 'active': active, 'room' : room}
    print(data)
    return JsonResponse(data)

def refreshHomeTable(request):
    rooms = request.META['QUERY_STRING']
    refreshed_rooms = []
    rooms = rooms.replace('[', '').replace(']', '')
    rooms = rooms.split(",")
    print(rooms)
    for room in rooms:
        print(room)
        peoplecount, inuse, timestamp = getPeopleCountAndUsage(room)
        if time.time() - timestamp > 60:
            active = 0
        else:
            active = 1
        refreshed_rooms.append((room, peoplecount, inuse, active))
        print(refreshed_rooms)
    data = {'rooms': refreshed_rooms}
    return JsonResponse(data) 
        
def bucketHeatMapData(heatmap): 
    for face in heatmap:
        print(face)
    

 
    
    
    
