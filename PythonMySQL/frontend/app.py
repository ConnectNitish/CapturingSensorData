from flask import Flask, render_template, redirect, request, url_for
import requests, json, atexit, time, plotly, plotly.graph_objs as go
import random
from flask import jsonify
import os,sys,inspect
import csv
from werkzeug import secure_filename
import psycopg2
from datetime import datetime
import datetime


current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
import BusinessLayer as  bl


from werkzeug import secure_filename



UPLOAD_FOLDER = current_dir

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 

max_size = 20
days = 10
user_hash_list = []

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

    

    return render_template("home.html",info = info, user_list = user_list)

@app.route('/navigate_to_user/<user_hash>', methods=['GET', 'POST']) 
def navigate_to_user(user_hash):
    bLayerObj = bl.BusinessLayer()
    user_list = bLayerObj.getAllUserHashDistinct()

    print("user_list: ",user_list)



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

    default_latitude,default_longitude,default_threshold_value = bLayerObj.get_default_location()

    return jsonify({'battery_timestamp': battery_timestamp,'battery_level':battery_level,
                   'call_state_count_list':call_state_count_list, 'call_state_list':call_state_list,
                   'location_longitude':location_longitude,'location_latitude':location_latitude,
                   'net_speed_timestamp':net_speed_timestamp,'net_speed':net_speed,'default_latitude':default_latitude,'default_longitude':default_longitude})


@app.route('/handle_data', methods=['POST'])
def handle_data():
	if request.method == 'POST':

		latitude_list = []
		longitude_list = []
		radius_list = []
		place_list = []

		f = request.files['file']
		f.save(secure_filename(f.filename))
		print("comming HERE ALWAYS -- ",f.filename)
		
		with open(f.filename) as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			indexx = 0
			for row in csv_reader:
				if(indexx!=0):	
					place_list.append(row[0])
					latitude_list.append(row[1])
					longitude_list.append(row[2])
					radius_list.append(row[3])
				indexx = indexx + 1
		
		print(radius_list)

		insert_popularLocationDB(place_list,latitude_list,longitude_list,radius_list)
			
		os.remove(f.filename)
	
	return redirect(url_for('popular_locations'))
	# return render_template('layout.html',data=user_hash_list,length=length)

@app.route("/popular_locations", methods = ['GET', 'POST'])
def popular_locations():
    global user_hash_list
    bLayerObj = bl.BusinessLayer()
    user_list = bLayerObj.getAllUserHashDistinct()
    place_list,latitude_list,longitude_list,radius_list = checkdbforpopularlocations()
    row_popular_locations = []
    length = 0
    if(len(radius_list)==0):
        row_popular_locations.append("no data to display")
    else:
        for i in range(0,len(radius_list)):
            temp_list = []
            temp_list.append(place_list[i])
            temp_list.append(latitude_list[i])
            temp_list.append(longitude_list[i])
            temp_list.append(radius_list[i])
            row_popular_locations.append(temp_list)
        length = len(radius_list)

    print("MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM")
    print(user_hash_list)
    return render_template('popular_location.html',data=row_popular_locations,length=length,output=user_hash_list,op_length=len(user_hash_list), user_list = user_list)
		
@app.route("/clicked_row", methods = ['GET', 'POST'])
def clicked_row():
    global user_hash_list
    row =request.form.getlist("mydata[]") 
    print("ROWWWWWWWWWW")
    print(row)
    print(row[0])
    user_hash_list = []
    temp_list_n = []
    temp_list_n.append(row[0])
    temp_list_n.append(row[1])
    temp_list_n.append(row[2])
    temp_list_n.append(row[3])
    #user_hash_list.append(temp_list_n)
    temp_x = get_userhash_popularlocation_new(row)
    if(len(temp_x)==0):
        y = "no user found"
        temp_x.append(y)
        
    else:
        temp_x.append("synthetic user1")
    if(row[0]=="dummy"):
        print("RECEIVED DUMMY ",row[0])
        temp_x.append("it is refreshed")
    user_hash_list.append( temp_x )
    op_length = 0
    if(len(user_hash_list)>1):
        op_length=int(len(user_hash_list)/2)
    else:
        op_length = int(len(user_hash_list)/2)
    if(len(user_hash_list)==0):
        op_length = 0
    print("user_hash_list in clicked row")
    print(user_hash_list)
    print("asdasd  len  ",op_length)
    # place_list,latitude_list,longitude_list,radius_list = checkdbforpopularlocations()

    # user_hash_list_i = []
    # length_i = 0
    # if(len(radius_list)==0):
    #     user_hash_list_i.append("no data to display")
    # else:
    #     for i in range(0,len(radius_list)):
    #         temp_list = []
    #         temp_list.append(place_list[i])
    #         temp_list.append(latitude_list[i])
    #         temp_list.append(longitude_list[i])
    #         temp_list.append(radius_list[i])
    #         user_hash_list_i.append(temp_list)
    #     length_i = len(radius_list)

    # print(op_length)
    # print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
    # return render_template('popular_location.html',data=user_hash_list_i,length=length_i,output=user_hash_list,op_length=op_length, user_list = user_list)
    return redirect(url_for('popular_locations'))
		



##To bl

def checkdbforpopularlocations():
	place_list = []
	latitude_list = []
	longitude_list = []
	radius_list = []
	conn = psycopg2.connect(host='127.0.0.1',database='python_mysql',user='postgres',password='qwerty')
	cursor = conn.cursor()
	my_query = """ SELECT place,latitude,longitude,radius from popularlocations """
	print(my_query)
	cursor.execute(my_query)
	rows = cursor.fetchall()
	# print(rows)
	for r in rows:
		place_list.append(r[0])
		latitude_list.append(float(r[1]))
		longitude_list.append(float(r[2]))
		radius_list.append(float(r[3]))
		# print(r)
	print("********************")
	conn.commit() 
	conn.close()
	cursor.close()
	return place_list,latitude_list,longitude_list,radius_list

def createInsert(tname1,columnlist,columnlistpercents):
        sql_insert_query = " INSERT INTO " + tname1 + "(" + columnlist + ")" +   " VALUES ( " + columnlistpercents +")"
        print(sql_insert_query)
        return sql_insert_query

def insert_popularLocationDB(place_list,latitude_list,longitude_list,radius_list):
	

	conn = psycopg2.connect(host='127.0.0.1',database='python_mysql',user='postgres',password='qwerty')
	cursor = conn.cursor()
	
	# print("----------------------------")
	# print(rows)
	col_str = "place,latitude,longitude,radius"
	s_str = "%s,%s,%s,%s"
	sql_insert_query = createInsert('popularlocations',col_str,s_str)
	for i in range(0,len(radius_list)):
		cursor.execute("""select place from popularlocations where latitude="""+"'"+str(latitude_list[i])+"'"+""" AND longitude="""+"'"+str(longitude_list[i])+"'"+""" AND radius="""+"'"+str(radius_list[i])+"'")
		conn.commit() # <--- makes sure the change is shown in the database
		rows = cursor.fetchall()
		if(len(rows)==0):
			record_list = []
			record_list.append(str(place_list[i]))
			record_list.append(str(latitude_list[i]))
			record_list.append(str(longitude_list[i]))
			record_list.append(str(radius_list[i]))
			print(record_list)
			result = cursor.execute(sql_insert_query, record_list)
			print(result)
			conn.commit() 
		else:
			print("DUPLICATE RECORD IN INPUT CSV FILE")
			print(rows)
	conn.close()
	cursor.close()



def get_userhash_popularlocation(range_list):
	#conn = psycopg2.connect("dbname='mydb3' user='dbuser' password='qwerty'")
	conn = psycopg2.connect(host='127.0.0.1',database='python_mysql',user='postgres',password='qwerty')
	cursor = conn.cursor()
	user_hash_list = []
	for i in range(0,len(range_list)):
		min_latitude = range_list[i]["latitude"][0]
		max_latitude = range_list[i]["latitude"][1]
		min_longitude = range_list[i]["longitude"][0]
		max_longitude = range_list[i]["longitude"][1]
		print(min_latitude,max_latitude)
		print(min_longitude,max_longitude)
		# min_longitude = -122.0
		# max_longitude = -122.1
		# min_latitude = 37.0
		# max_latitude = 37.5219983333333

		# print(min_latitude,min_longitude,max_latitude,max_longitude)
		till_date = 10
		dt = datetime.datetime.today() - datetime.timedelta(till_date)
		dt = dt.timestamp()
		my_query = """ SELECT DISTINCT userhash from location where cast(longitude as float)>="""+str(min_longitude)+ """ AND  cast(longitude as float)<="""+str(max_longitude)+ """ AND cast(latitude as float)>="""+str(min_latitude)+""" AND cast(latitude as float)<="""+str(max_latitude) 
		print(my_query)
		cursor.execute(my_query)
		# self.my_cursor.execute("""SELECT DISTINCT battery.userhash,battery.level,battery.timestamp FROM battery,(select userhash,count(distinct level) as countlevel from (SELECT * FROM battery WHERE timestamp >= """ + "'"+ str(dt) +"'"+ """) B group by userhash order by countlevel desc limit 3) AA WHERE AA.userhash = battery.userhash AND battery.timestamp >= """ + "'" + str(dt) + "'" + """ ORDER BY battery.userhash,battery.timestamp """)
		rows = cursor.fetchall()
		if(len(rows)>0):
			for r in rows:
				if(len(r)>0):
					for rr in r:
						user_hash_list.append(rr)
		print(user_hash_list)
		conn.commit() 
	print("--------------------------------++++++++++++++++++++++++++")
	conn.close()
	cursor.close()
	return user_hash_list

def get_userhash_popularlocation_new(row_list):

	conn = psycopg2.connect(host='127.0.0.1',database='python_mysql',user='postgres',password='qwerty')
	cursor = conn.cursor()
	min_latitude = float(row_list[1]) - float(row_list[3])
	max_latitude = float(row_list[1]) + float(row_list[3])
	min_longitude = float(row_list[2]) - float(row_list[3])
	max_longitude = float(row_list[2]) + float(row_list[3])
	user_hash_list = []
	till_date = 10
	dt = datetime.datetime.today() - datetime.timedelta(till_date)
	dt = dt.timestamp()
	my_query = """ SELECT DISTINCT userhash from location where cast(longitude as float)>="""+str(min_longitude)+ """ AND  cast(longitude as float)<="""+str(max_longitude)+ """ AND cast(latitude as float)>="""+str(min_latitude)+""" AND cast(latitude as float)<="""+str(max_latitude) 
	print(my_query)
	cursor.execute(my_query)
	rows = cursor.fetchall()
	if(len(rows)>0):
		for r in rows:
			if(len(r)>0):
				for rr in r:
					user_hash_list.append(rr)
	print("user_hash_list in funct-> ",user_hash_list)
	conn.close()
	cursor.close()
	return user_hash_list





if __name__ == '__main__':
    app.run(debug=True,port=3904,host="0.0.0.0")
