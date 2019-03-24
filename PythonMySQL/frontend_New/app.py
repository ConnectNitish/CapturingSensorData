from flask import Flask, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from pusher import Pusher
import requests, json, atexit, time, plotly, plotly.graph_objs as go
import random

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
import SaveData as sd

# create flask app
app = Flask(__name__)

# global max_size
max_size = 20

# configure pusher object
pusher = Pusher(
    app_id='741064',
    key='00bd2d16b44796f46ee2',
    secret='badf32c83598faac5911',
    cluster='ap2',
    ssl=True
)


global user_hash, call_state_types, battery_probe, call_state, battery_timestamp, call_state_timestamp,gps_timestamp

global latitude_list, longitude_list, place_list

user_hash = ""
probe_list = ["battery","callstate","location"]
call_state_types = ["Idle","Offhook","Ringing"]
call_state_types_lower = ["idle","off-hook","ringing"]
battery_probe = []
call_state = [0,0,0]
battery_timestamp = []
call_state_timestamp = []
gps_timestamp = []
latitude_list = []
longitude_list = []
place_list = []

@app.route("/")
def index():
    return render_template("index.html")


def retrieve_data():

    global user_hash, call_state_types, battery_probe, call_state, battery_timestamp, call_state_timestamp,gps_timestamp
    global latitude_list, longitude_list, place_list

    #probe_data = chitta_function()
    probe_data = sd.InvokeDBFunc()

    if len(user_hash) == 0:

        for probe in probe_list:

            if probe not in probe_data:
                continue

            for key,value in probe_data[probe].items():

                user_hash = key
                break 
            
            if len(user_hash) == 0:
                break 

    print()
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print "user_hash: ",user_hash     
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print()
    

    for probe in probe_list:
        
        if probe not in probe_data:
            continue

        if probe == "battery":
            print("Probe: ",probe)
            if user_hash in probe_data[probe]:

                battery_level, timestamp = probe_data[probe][user_hash]
                
                battery_probe.append(battery_level)
                battery_timestamp.append(timestamp)                

                if len(battery_probe) > max_size:

                    battery_probe = battery_probe[1:len(battery_probe)]
                    battery_timestamp = battery_timestamp[1:len(battery_timestamp)]

            else:
                # print()
                # print()
                # print "#########################################"

                # print user_hash

                # print()
                # print()

                # print probe_data[probe][user_hash]

                # print "#########################################"
                # print()
                # print()
                print("Battery probe data does not contains information regarding user: ",user_hash)
            print("End Probe: ",probe)
        elif probe == "callstate":
            # print("Probe: ",probe)
            if user_hash in probe_data[probe]:            

                cstate,timestamp  = probe_data[probe][user_hash]

                print "call_state------------: ", cstate
                
                call_state[call_state_types_lower.index(cstate)] += 1
               
                call_state_timestamp.append(timestamp)
                
                if len(call_state_timestamp) > max_size:
                    call_state_timestamp = call_state_timestamp[1:len(call_state_timestamp)]
               
            else:
                print("Call state probe data does not contains information regarding user: ",user_hash)
            print("End Probe: ",probe)
        elif probe == "location":
            print("Probe: ",probe)
            if user_hash in probe_data[probe]:

                longitude,latitude, timestamp = probe_data[probe][user_hash]

                latitude_list.append(latitude)
                longitude_list.append(longitude)
                gps_timestamp.append(timestamp)
                # place_list.append("Hyderabad")

                if len(gps_timestamp) > max_size:

                    latitude_list = latitude_list[1:len(latitude_list)]
                    longitude_list = longitude_list[1:len(longitude_list)]
                    gps_timestamp = gps_timestamp[1:len(gps_timestamp)]         
                    # place_list = place_list[1:len(place_list)] 
            else:
                print("GPS probe data does not contains information regarding user: ",user_hash)
           
    battery_data = [go.Scatter(
        x = battery_timestamp,
        y = battery_probe
    )]

  

    call_state_data = [go.Pie(
        labels = call_state_types,
        values = call_state
    )]

 

    data = {
        'battery': json.dumps(list(battery_data), cls=plotly.utils.PlotlyJSONEncoder),
        'call_state': json.dumps(list(call_state_data), cls=plotly.utils.PlotlyJSONEncoder),
        'latitude': json.dumps(list(latitude_list)),
        'longitude': json.dumps(list(longitude_list)),
        'place': json.dumps(list(place_list))
    }

    print("$$$$$$$$$$$$$$$$$$$$$$$$")
    print(data)     

    # trigger event
    pusher.trigger("my-channel", "my-event", data)



scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=retrieve_data,
    trigger=IntervalTrigger(seconds=10),
    id='prices_retrieval_job',
    name='Retrieve prices every 10 seconds',
    replace_existing=True)
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())



if __name__ == '__main__':
    app.run(debug=True,use_reloader=False,port=7000)
