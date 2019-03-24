from flask import Flask, render_template, redirect, request
import requests, json, atexit, time, plotly, plotly.graph_objs as go
import random
from flask import jsonify
import os,sys,inspect
# current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# parent_dir = os.path.dirname(current_dir)
# sys.path.insert(0, parent_dir) 
# import SaveData as sd

# create flask app
app = Flask(__name__)

# global max_size
max_size = 20


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/retrieve_data")
def retrieve_data():

    

@app.route('/retrieve_user_data/<user_hash>', methods=['GET', 'POST']) 
def retrieve_user_data(user_hash):
    
    probe_list = ["battery","callstate","location"]
    
    call_state_list = ["Idle","Offhook","Ringing"]
    call_state_types_lower = ["idle","off-hook","ringing"]
    call_state_count_list = [0,0,0]
    call_state_timestamp = []
    
    battery_probe = []
    battery_timestamp = []
    
    gps_timestamp = []
    latitude_list = []
    longitude_list = []
    
    net_speed_timestamp = []
    net_speed = []
    

    for probe in probe_list:
        
        if probe not in probe_data:
            continue

        if probe == "battery":
            
            battery_probe_data = 

            battery_probe = battery_probe_data["level"]
            battery_timestamp = battery_probe_data["time"]

        elif probe == "NetworkProbe":

            net_probe_data = get_network_probe_data(user_hash)

            net_speed = net_probe_data["speed"]     
            net_speed_timestamp = net_probe_data["time"]

        elif probe == "callstate":
            
            call_state_data_probe = 

            call_state_count_list[0] = call_state_data_probe["ringing"]
            call_state_count_list[1] = call_state_data_probe["off-hook"]
            call_state_count_list[2] = call_state_data_probe["idle"]
            
        elif probe == "location":
            
            location_data_probe = 
            
            gps_timestamp = location_data_probe["timestamp"]
            location_latitude = location_data_probe["latitude"]
            location_longitude = location_data_probe["longitude"]


    return jsonify({'battery_timestamp': battery_timestamp,'battery_level':battery_level,
                   'call_state_count_list':call_state_count_list, 'call_state_list':call_state_list,
                   'location_longitude':location_longitude,'location_latitude':location_latitude,
                   'net_speed_timestamp':net_speed_timestamp,'net_speed':net_speed})

                


if __name__ == '__main__':
    app.run(debug=True,port=7000)
