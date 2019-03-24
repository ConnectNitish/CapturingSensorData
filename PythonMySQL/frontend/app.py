from flask import Flask, render_template, redirect, request, url_for
import requests, json, atexit, time, plotly, plotly.graph_objs as go
import random
from flask import jsonify
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
import BusinessLayer as  bl
# create flask app
app = Flask(__name__)

# global max_size
max_size = 20
# days
days = 2

@app.route("/")
def index():
    return render_template("index.html")

# @app.route("/retrieve_data")
# def retrieve_data():

    

@app.route('/retrieve_user_data/<user_hash>', methods=['GET', 'POST']) 
def retrieve_user_data(user_hash):
    
    print("Request received")

    probe_list = ["battery","callstate","location","network"]
    
    call_state_list = ["Idle","Off-hook","Ringing"]
    call_state_types_lower = ["idle","off-hook","ringing"]
    call_state_count_list = [0,0,0]
    call_state_timestamp = []
    
    battery_level = []
    battery_timestamp = []
    
    gps_timestamp = []
    latitude_list = []
    longitude_list = []
    
    net_speed_timestamp = []
    net_speed = []

        
    bLayerObj = bl.BusinessLayer()
        
    battery_probe_data = bLayerObj.get_battery_details_for_user(user_hash,days)

    battery_level = battery_probe_data["level"]
    battery_timestamp = battery_probe_data["timestamp"]

    

    # elif probe == "NetworkProbe":

    net_probe_data = bLayerObj.get_wifi_details_for_user(user_hash,days)

    net_speed = net_probe_data["speed"]     
    net_speed_timestamp = net_probe_data["timestamp"]

    # elif probe == "callstate":
    #
    call_state_data_probe = bLayerObj.get_callstate_details_for_user(user_hash,days)

    call_state_count_list[2] = call_state_data_probe["ringing"]
    call_state_count_list[1] = call_state_data_probe["off-hook"]
    call_state_count_list[0] = call_state_data_probe["idle"]
        
    # elif probe == "location":
        
    location_data_probe = bLayerObj.get_location_details_for_user(user_hash,days)
    
    gps_timestamp = location_data_probe["timestamp"]
    location_latitude = location_data_probe["latitude"]
    location_longitude = location_data_probe["longitude"]


    return jsonify({'battery_timestamp': battery_timestamp,'battery_level':battery_level,
                   'call_state_count_list':call_state_count_list, 'call_state_list':call_state_list,
                   'location_longitude':location_longitude,'location_latitude':location_latitude,
                   'net_speed_timestamp':net_speed_timestamp,'net_speed':net_speed})

                


if __name__ == '__main__':
    app.run(debug=True,port=7000)
