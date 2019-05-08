import json
from pprint import pprint
import re
import database as db
import shutil
import os
import datetime


battery_cols = ["userhash" ,"icon_small" ,"invalid_charger" ,"level" ,"health" ,"scale" ,"priority" ,"technology" , "charge_counter" ,"max_charging_current" ,"probe_transmit_mode" ,"voltage" ,"timestamp" ,"temperature" ,"max_charging_voltage" ,"present" ,"battery_low" ,"plugged" ,"seq" ,"status"]
callstate_cols = ["userhash" ,"call_state" ,"timestamp" ,"probe_transmit_mode" ]
datecalender_cols = ["userhash" ,"day_of_year" ,"month" ,"dst_offset" ,"day_of_month" ,"week_of_month" ,"probe_transmit_mode" ,"day_of_week_in_month"  ,"week_of_year"  ,"hour_of_day"  ,"timestamp"  ,"minute"  ,"day_of_week"]
network_cols = ["userhash"  ,"interface_name"  , "interface_display"  , "hostname"  , "timestamp"  , "ip_address"  ,"probe_transmit_mode"]
wakelockinformation_cols = ["userhash"  ,"bright_count"  ,"dim_locks"  , "partial_count"  ,"timestamp"  , "full_locks"  , "bright_locks"  , "partial_locks"  , "dim_count"  , "probe_transmit_mode"   , "full_count"]
wifiaccesspoints_cols = ["userhash"  ,"current_rssi"  , "timestamp"  , "current_bssid"  ,"access_point_count"  ,"probe_transmit_mode"  ,"current_link_speed"  , "current_ssid" ]
sunrisesunsetfeature_cols = ["userhash"  ,"sunset"  , "timestamp"  , "longitude"  ,"sunrise"  ,"is_day"  ,"sunrise_distance"  ,"sunset_distance"  ,"probe_transmit_mode"  , "latitude"  ,"day_duration" ]
location_cols = ["userhash"  ,"time_fix"  , "longitude"  ,"altitude"  ,"probe_transmit_mode"  , "accuracy"  , "gps_available"  ,"speed"  ,"timestamp"  , "provider"  ,"network_available"  ,"bearing"  ,"latitude"]

def isColPresent(tname,key):
    key = key.lower()
    if(tname.find("BatteryProbe")!=-1):
        if(key in battery_cols):
            return True

    if(tname.find("CallStateProbe")!=-1):
        if(key in callstate_cols):
            return True
    if(tname=="DateCalendarProbe"):
        if(key in datecalender_cols):
            return True
    if(tname=="NetworkProbe"):
        if(key in network_cols):
            return True
    if(tname=="WakeLockInformationProbe"):
        if(key in wakelockinformation_cols):
            return True
    if(tname=="WifiAccessPointsProbe"):
        if(key in wifiaccesspoints_cols):
            return True
    if(tname=="SunriseSunsetFeature"):
        if(key in sunrisesunsetfeature_cols):
            return True
    if(tname=="LocationProbe"):
        if(key in location_cols):
            return True
    
    return False

def timeStamped(fname, fmt='%Y-%m-%d-%H-%M-%S_{fname}'):
    return datetime.datetime.now().strftime(fmt).format(fname=fname)

def writeLog(message):
	log_file="log_file"
	exists = os.path.isfile(log_file)	
	if not exists:
		handler = open(log_file,'w')
		handler.write(timeStamped(""))
		handler.write(message)
		handler.write("\n")

def InvokeDBFunc():
	newobj = db.Database("127.0.0.1",'python_mysql','postgres','test')
	x = newobj.probe_info()
	print(x)
	newobj.close_conn_cursor()
	return x

class SaveData:

	def SaveDataToDB(self):
		try:

			#newobj = db.Database("127.0.0.1",'mydb3','dbuser','qwerty')
			newobj = db.Database("127.0.0.1",'python_mysql','postgres','test')
			# newobj.printRows("schema1.table1")
			getCurrentTimeStamp = timeStamped("")
			name_of_file_to_Store="Input_feed.json"

			#with open('My_Phone_Data.json') as f:
			#with open('2019-03-21-13-29-54_data_By_app_2.json') as f:
			with open(name_of_file_to_Store) as f:
			    data = json.load(f)

			# pprint(data)
			userdata = data["UserHash"]
			# print(userdata)
			payload = data["Payload"]
			# print(type(payload))

			payload_json = json.loads(payload)
			# pprint(payload_json)

			payload_dict = {}

			for item in payload_json:

				# print(item)
				# print("####################################################################")

				probe_dict = {}

				tname = re.split('[.]',item["PROBE"])[-1]
				# print("tname is ----",tname)
				# print(re.split('[.]',item["PROBE"]))

				if(tname!="SoftwareInformationProbe"):
					payload_dict[tname] = []
				record = []
				record.append(userdata)
				
				for key,values in item.items():
					if key != "PROBE":
						if key!= "GUID" and key!="ACCESS_POINTS":
							record.append(str(values))
						if(tname!="SoftwareInformationProbe"):
							payload_dict[tname].append((key,values))

			# pprint(payload_dict)

			for k,v in payload_dict.items():
				col_str = ""
				record_list = []
				s_str = ""

				col_str+="userhash"
				record_list.append(str(userdata).lower())
				col_str+=","
				s_str+="%s,"
				print(k)
				for myval in v:
					if(isColPresent(k,myval[0])):
						col_str+=str(myval[0]).lower()
						record_list.append(str(myval[1]).lower())
						col_str+=","
						s_str+="%s,"
				col_str = col_str[:len(col_str)-1]
				s_str = s_str[:len(s_str)-1]
				# record_str = record_str[:len(record_str)-1]
				print("col_str ::",col_str)
				print(s_str)
				print(record_list)
				print("-----------------IN LAYER HI--------------------------")
				newobj.insert(k,col_str,s_str,tuple(record_list),name_of_file_to_Store)
				print("-----------------IN LAYER HI 2--------------------------")

			newobj.close_conn_cursor()

			#move the file to back up Folder 
			destination_directory = "./BackUp/"+getCurrentTimeStamp
			if not os.path.exists(destination_directory):
				os.makedirs(destination_directory)
			print("GOOD---------------------")
			shutil.move(name_of_file_to_Store, destination_directory)
			
		except:
			#Some Error Occurered 
			print("-------------------------------EX------------------------------------------")
			writeLog("--- Parsing File Problem ---- "+getCurrentTimeStamp)
			#move the file to back up Folder 
			destination_directory = "./Error/"+getCurrentTimeStamp
			if not os.path.exists(destination_directory):
			    os.makedirs(destination_directory)
			shutil.move(name_of_file_to_Store, destination_directory)
			newobj.close_conn_cursor()			

			#pprint(payload_dict)

		# d = payload_dict['WakeLockInformationProbe']

		# for item in d:

		# 	print(item)

if __name__ == "__main__":
	SaveDataobj = SaveData()
	SaveDataobj.SaveDataToDB()
	# InvokeDBFunc()
	
