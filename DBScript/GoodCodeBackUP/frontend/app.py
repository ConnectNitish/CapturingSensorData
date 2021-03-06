from flask import Flask, render_template, redirect, request, url_for
import requests, json, atexit, time, plotly, plotly.graph_objs as go
import random
from flask import jsonify
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
import BusinessLayer as  bl

app = Flask(__name__)

max_size = 20
days = 5

@app.route("/")
def index():

    bLayerObj = bl.BusinessLayer()

    networkInfo = bLayerObj.getNetworkDetailsForPresentation()
    wifi= bLayerObj.getWifiDataForPresentation()

    info = {
        "networkInfo":networkInfo,
        "wifi":wifi
    }

    user_list = bLayerObj.getAllUserHashDistinct()

    print("user_list: ",user_list)

    # user_list = ['068fd0571f7cc527d4983d35f0d908d9', 'fde62956f023ab40685ecceee22c402e', 'b50f1867e01b21d3134b0097ecb7990d', 
    # '73803249c6667c5af2d51c0dedfae487', 'e251a758734abbefe63347192e64ed9f', 'a269f1b41ae5073302d70baac6137ae2', 
    # '34237272481aa6a02ea94799695a6982', '67d97bd65bfff6f9274ef52034fa0e19', '93e2f4935402da5361fcaeb636fc6cd2']

    return render_template("home.html",info = info, user_list = user_list)


@app.route('/navigate_to_user/<user_hash>', methods=['GET', 'POST']) 
def navigate_to_user(user_hash):
    bLayerObj = bl.BusinessLayer()
    user_list = bLayerObj.getAllUserHashDistinct()

    print("user_list: ",user_list)

    # user_list = ['068fd0571f7cc527d4983d35f0d908d9', 'fde62956f023ab40685ecceee22c402e', 'b50f1867e01b21d3134b0097ecb7990d', 
    # '73803249c6667c5af2d51c0dedfae487', 'e251a758734abbefe63347192e64ed9f', 'a269f1b41ae5073302d70baac6137ae2', 
    # '34237272481aa6a02ea94799695a6982', '67d97bd65bfff6f9274ef52034fa0e19', '93e2f4935402da5361fcaeb636fc6cd2']

    return render_template("index.html", user_hash = user_hash, user_list = user_list)

#used at home page for 5 users only
@app.route("/retrieve_data", methods=['GET', 'POST'])
def retrieve_data():

    print("From home.html")

    bLayerObj = bl.BusinessLayer()

    #latitude_temp,longitude_temp,threshold_value = [17.445437,78.3456945,0.0035]
    latitude_temp,longitude_temp,threshold_value = bLayerObj.get_default_location()
    print(latitude_temp,longitude_temp,threshold_value)
    active_user_data = bLayerObj.getBatteryInfoForAllUser()
    location_based_user_data = bLayerObj.getBatteryInfoForAllUserAsPerLocation(latitude_temp,longitude_temp,threshold_value)

    print(location_based_user_data)

    data_dict = {"active_user_data" : active_user_data,"location_based_user_data":location_based_user_data}

    return jsonify(data_dict)
    
#specific to a particular user
@app.route('/retrieve_user_data/<user_hash>', methods=['GET', 'POST']) 
def retrieve_user_data(user_hash):
    
    print("Request received")
    print(user_hash)

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


    net_probe_data = bLayerObj.get_wifi_details_for_user(user_hash,days)

    net_speed = net_probe_data["speed"]     
    net_speed_timestamp = net_probe_data["timestamp"]

    
    call_state_data_probe = bLayerObj.get_callstate_details_for_user(user_hash,days)

    call_state_count_list[0] = call_state_data_probe["idle"]
    call_state_count_list[1] = call_state_data_probe["off-hook"]
    call_state_count_list[2] = call_state_data_probe["ringing"]
        
    
    location_data_probe = bLayerObj.get_location_details_for_user(user_hash,days)
    
    gps_timestamp = location_data_probe["timestamp"]
    location_latitude = location_data_probe["latitude"]
    location_longitude = location_data_probe["longitude"]


    return jsonify({'battery_timestamp': battery_timestamp,'battery_level':battery_level,
                   'call_state_count_list':call_state_count_list, 'call_state_list':call_state_list,
                   'location_longitude':location_longitude,'location_latitude':location_latitude,
                   'net_speed_timestamp':net_speed_timestamp,'net_speed':net_speed})

                


if __name__ == '__main__':
    app.run(debug=True,port=3904,host="0.0.0.0")
