#import mysql.connector
#from mysql.connector import Error
import psycopg2
from datetime import datetime
import datetime

class Database:
    my_cursor = None
    conn = None
    def __init__(self,host,dbname,user,pwd):
        self.host = host
        self.dbname = dbname
        self.user  = user
        self.password = pwd
        self.conn = psycopg2.connect(host=host,
                                    database=dbname,
                                    user=user,
                                    password=pwd)
        self.my_cursor =  self.conn.cursor()

    def probe_info(self,userhash):
        ret_dict = {}
        x1 = self.get_battery()
        #print(x1)
        uids = {}
        for r in x1:
            dt_object = datetime.datetime.fromtimestamp(int(r[2]))
            if(r[0]==userhash):
                uids[r[0]] = [r[1],str(dt_object)]
            # print(r[0])
        if(x1):
            ret_dict["battery"]=uids
        # print(ret_dict)
        # print("----------------------------")
        x2 = self.get_callState()
        uids = {}
        for r in x2:
            dt_object = datetime.datetime.fromtimestamp(int(r[2]))
            if(r[0]==userhash):
                uids[r[0]] = [r[1],str(dt_object)]
            # print(r[0])
        if(x2):
            ret_dict["callstate"]=uids
        # print(uids)
        # print("----------------------------")
        x3 = self.get_location()
        uids = {}
        for r in x3:
            dt_object = datetime.datetime.fromtimestamp(int(r[3]))
            if(r[0]==userhash):
                uids[r[0]] = [r[1],r[2],str(dt_object)]
            # print(r[0])
        if(x3):
            ret_dict["location"]=uids
        # print(uids)
        return ret_dict

    
    def get_battery(self):
        self.my_cursor.execute("""select userhash,scale,timestamp from battery order by timestamp""")
        rows = self.my_cursor.fetchall()
        # print(rows)
        return rows
    
    def get_callState(self):
        self.my_cursor.execute("""select userhash,call_state,timestamp from callstate order by timestamp""")
        rows = self.my_cursor.fetchall()
        # print(rows)
        return rows

    def get_location(self):
        self.my_cursor.execute("""select userhash,longitude,latitude,timestamp from location order by timestamp""")
        rows = self.my_cursor.fetchall()
        # print(rows)
        return rows
    
    def getWifiDataForPresentation(self):
        self.my_cursor.execute("""select DISTINCT current_bssid,current_link_speed,access_point_count,current_ssid,userhash from wifiaccesspoints
order by userhash """)
        rows = self.my_cursor.fetchall()
        # print(rows)
        return rows

    def getNetworkDetailsForPresentation(self):
        self.my_cursor.execute("""select hostname,IP_address,userhash from network WHERE interface_name!='' order by userhash""")
        rows = self.my_cursor.fetchall()
        # print(rows)
        return rows

    def printRows(self,tname):
        if(tname == "CallStateProbe"):
            self.my_cursor.execute("""select * from callstate""")
            rows = self.my_cursor.fetchall()
            print(rows)
        elif(tname == "DateCalendarProbe"):
            self.my_cursor.execute("""select * from datecalendar""")
            rows = self.my_cursor.fetchall()
            print(rows)
        elif(tname == "NetworkProbe"):
            self.my_cursor.execute("""select * from network""")
            rows = self.my_cursor.fetchall()
            print(rows)
        elif(tname == "WakeLockInformationProbe"):
            self.my_cursor.execute("""select * from wakelockinformation""")
            rows = self.my_cursor.fetchall()
            print(rows)
        elif(tname == "BatteryProbe"):
            self.my_cursor.execute("""select * from battery""")
            rows = self.my_cursor.fetchall()
            print(rows)
        elif(tname == "WifiAccessPointsProbe"):
            self.my_cursor.execute("""select * from wifiaccesspoints""")
            rows = self.my_cursor.fetchall()
            print(rows)
        elif(tname == "SunriseSunsetFeature"):
            self.my_cursor.execute("""select * from sunrisesunsetfeature""")
            rows = self.my_cursor.fetchall()
            print(rows)
        elif(tname == "LocationProbe"):
            self.my_cursor.execute("""select * from location""")
            rows = self.my_cursor.fetchall()
            print(rows)

    def createInsert(self,tname1,columnlist,columnlistpercents):
        sql_insert_query = " INSERT INTO " + tname1 + "(" + columnlist + ")" +   " VALUES ( " + columnlistpercents +")"
        print(sql_insert_query)
        return sql_insert_query

    def insert(self,tname,col_str,s_str,record_list,myf):
        sql_insert_query = ""
        # print("tname ",tname)
        if(tname == "CallStateProbe"):
            print("values to insert-----------------------")
            print(record_list)
            # print("=====================================")
            sql_insert_query = self.createInsert('callstate',col_str,s_str)
            # sql_insert_query = """ INSERT INTO callstate (userhash,call_state ,timestamp ,probe_transmit_mode) 
            #                VALUES (%s,%s,%s,%s) """

        elif(tname == "DateCalendarProbe"):
            print("values to insert-----------------------")
            print(record_list)
            # print("=====================================")
            # sql_insert_query = """ INSERT INTO datecalendar (userhash,day_of_year,month,dst_offset,day_of_month,week_of_month,probe_transmit_mode,day_of_week_in_month,week_of_year,hour_of_day,timestamp,minute ,day_of_week) 
            #                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """
            sql_insert_query = self.createInsert('datecalendar',col_str,s_str)


        elif(tname == "NetworkProbe"):
            print("values to insert-----------------------")
            print(record_list)
            # print("=====================================")
            # sql_insert_query = """ INSERT INTO network (userhash,interface_name , interface_display , hostname , timestamp , ip_address ,probe_transmit_mode) 
            #                VALUES (%s,%s,%s,%s,%s,%s,%s) """
            sql_insert_query = self.createInsert('network',col_str,s_str)

        elif(tname == "WakeLockInformationProbe"):
            print("values to insert-----------------------")
            print(record_list)
            # print("=====================================")
            # sql_insert_query = """ INSERT INTO wakelockinformation (userhash,bright_count ,dim_locks, partial_count ,timestamp, full_locks, bright_locks, partial_locks, dim_count, probe_transmit_mode , full_count) 
            #                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """
            sql_insert_query = self.createInsert('wakelockinformation',col_str,s_str)

        elif(tname == "BatteryProbe"):
            print("values to insert-----------------------")
            print(record_list)
            # print("=====================================")
            # sql_insert_query = """ INSERT INTO battery (userhash,icon_small ,invalid_charger ,level ,health ,scale ,priority ,technology , charge_counter ,max_charging_current ,probe_transmit_mode ,voltage ,timestamp ,temperature ,max_charging_voltage ,present ,battery_low ,plugged ,seq ,status ) 
            #                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """
            sql_insert_query = self.createInsert('battery',col_str,s_str)

        elif(tname == "WifiAccessPointsProbe"):
            print("values to insert-----------------------")
            print(record_list)
            # print("=====================================")
            # sql_insert_query = """ INSERT INTO wifiaccesspoints (userhash,current_rssi , timestamp , current_bssid ,access_point_count ,probe_transmit_mode ,current_link_speed , current_ssid  ) 
            #                VALUES (%s,%s,%s,%s,%s,%s,%s,%s) """
            sql_insert_query = self.createInsert('wifiaccesspoints',col_str,s_str)

        elif(tname == "SunriseSunsetFeature"):
            print("values to insert-----------------------")
            print(record_list)
            # print("=====================================")
            # sql_insert_query = """ INSERT INTO sunrisesunsetfeature (userhash,sunset , timestamp , longitude ,sunrise ,is_day ,sunrise_distance ,sunset_distance,probe_transmit_mode , latitude ,day_duration  ) 
            #                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """
            sql_insert_query = self.createInsert('sunrisesunsetfeature',col_str,s_str)


        elif(tname == "LocationProbe"):
            print("values to insert-----------------------")
            print(record_list)
            # print("=====================================")
            # sql_insert_query = """ INSERT INTO location (userhash ,time_fix , longitude ,altitude ,probe_transmit_mode , accuracy , gps_available ,speed ,timestamp , provider ,network_available ,bearing ,latitude  ) 
            #                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """
            sql_insert_query = self.createInsert('location',col_str,s_str)

        print()

        if(sql_insert_query!=""):
            try:
                result = self.my_cursor.execute(sql_insert_query, record_list)
                print(result)
            except:
                print("failed insert for table ",tname," for file ",myf)
            # self.my_cursor.execute("""insert into """+tname+""" (id,password) values("""+str(a)+""","""+b+""")""" )
            self.conn.commit()
        else:
            print("new probe found with tname------",tname)

    
    def get_battery_details_for_user(self,userhash,till_date=1):
        dt = datetime.datetime.today() - datetime.timedelta(till_date)
        dt = dt.timestamp()
        self.my_cursor.execute("""select userhash,level,timestamp from battery where userhash="""+"'"+(userhash)+"'"+"""and timestamp >= """+"'"+str(dt) +"' order by timestamp")
        rows = self.my_cursor.fetchall()
        level_list = []
        timestamp_list = []
        for r in rows:
            level_list.append(r[1])
            timestamp_list.append(r[2])
        ret_dict = {}
        ret_dict["level"] = level_list
        ret_dict["timestamp"] = timestamp_list
        return ret_dict 
    
    
    def get_callstate_details_for_user(self,userhash,till_date=5):
        dt = datetime.datetime.today() - datetime.timedelta(till_date)
        dt = dt.timestamp()
        self.my_cursor.execute("""select userhash,call_state,timestamp from callstate where userhash="""+"'"+(userhash)+"'"+"""and timestamp >= """+"'"+str(dt) +"'")
        rows = self.my_cursor.fetchall()
        callstate_list = []
        timestamp_list = []
        for r in rows:
            callstate_list.append(r[1])
            timestamp_list.append(r[2])
        unique_call_states = []
        for r in callstate_list:
            if(r not in unique_call_states):
                unique_call_states.append(r)
        ret_dict = {}
        for call_s in unique_call_states:
            ret_dict[call_s] = callstate_list.count(call_s)

        
        # print(ret_dict)
        
        return ret_dict 


    def get_wifi_details_for_user(self,userhash,till_date=1):
        dt = datetime.datetime.today() - datetime.timedelta(till_date)
        dt = dt.timestamp()
        self.my_cursor.execute("""select userhash,current_link_speed,timestamp from wifiaccesspoints where userhash="""+"'"+(userhash)+"'"+"""and timestamp >= """+"'"+str(dt) +"' order by timestamp")
        rows = self.my_cursor.fetchall()
        current_link_speed_list = []
        timestamp_list = []
        for r in rows:
            current_link_speed_list.append(r[1])
            timestamp_list.append(r[2])
        ret_dict = {}
        ret_dict["speed"] = current_link_speed_list
        ret_dict["timestamp"] = timestamp_list
        return ret_dict 

    def get_location_details_for_user(self,userhash,till_date=1):
        dt = datetime.datetime.today() - datetime.timedelta(till_date)
        dt = dt.timestamp()
        self.my_cursor.execute("""select userhash,longitude,latitude,timestamp from location where userhash="""+"'"+(userhash)+"'"+"""and timestamp >= """+"'"+str(dt) +"'")
        rows = self.my_cursor.fetchall()
        latitude_list = []
        longitude_list = []
        timestamp_list = []
        for r in rows:
            latitude_list.append(r[2])
            longitude_list.append(r[1])
            timestamp_list.append(r[3])
        ret_dict = {}
        ret_dict["latitude"] = latitude_list
        ret_dict["longitude"] = longitude_list
        ret_dict["timestamp"] = timestamp_list
        return ret_dict 

    def getAllUserHash(self):
        ret_list = []
        self.my_cursor.execute("""select userhash from battery""")
        rows = self.my_cursor.fetchall()
        for r in rows:
            if(r[0] not in ret_list):
                ret_list.append(r[0])
        
        self.my_cursor.execute("""select userhash from callstate""")
        rows = self.my_cursor.fetchall()
        for r in rows:
            if(r[0] not in ret_list):
                ret_list.append(r[0])
        
        self.my_cursor.execute("""select userhash from datecalendar""")
        rows = self.my_cursor.fetchall()
        for r in rows:
            if(r[0] not in ret_list):
                ret_list.append(r[0])
        
        self.my_cursor.execute("""select userhash from network""")
        rows = self.my_cursor.fetchall()
        for r in rows:
            if(r[0] not in ret_list):
                ret_list.append(r[0])

        self.my_cursor.execute("""select userhash from wakelockinformation""")
        rows = self.my_cursor.fetchall()
        for r in rows:
            if(r[0] not in ret_list):
                ret_list.append(r[0])
        
        self.my_cursor.execute("""select userhash from wifiaccesspoints""")
        rows = self.my_cursor.fetchall()
        for r in rows:
            if(r[0] not in ret_list):
                ret_list.append(r[0])
        self.my_cursor.execute("""select userhash from sunrisesunsetfeature""")
        rows = self.my_cursor.fetchall()
        for r in rows:
            if(r[0] not in ret_list):
                ret_list.append(r[0])

        self.my_cursor.execute("""select userhash from location""")
        rows = self.my_cursor.fetchall()
        for r in rows:
            if(r[0] not in ret_list):
                ret_list.append(r[0])
        
        # print("ret_list")
        # print(ret_list)
        for r in ret_list:
            print("r = ",r)
            tlist = []
            tlist.append(r)
            myt = tuple(tlist)
            print("tlist",myt)
            sql_insert_query = """ INSERT INTO allusers (userhash) VALUES (%s)"""
            result = self.my_cursor.execute(sql_insert_query, myt)
            print(result)
            self.conn.commit()

        self.my_cursor.execute("""select userhash from allusers""")
        rows123 = self.my_cursor.fetchall()
        return rows123

	#Get Battery Info Of All User For Last 24 hrs 
    def getBatteryInforForAllUsers(self,till_date=5):
        dt = datetime.datetime.today() - datetime.timedelta(till_date)
        dt = dt.timestamp()
        # self.my_cursor.execute("""select userhash,longitude,latitude,timestamp from location where userhash="""+"'"+(userhash)+"'"+"""and timestamp >= """+"'"+str(dt) +"'")
        self.my_cursor.execute("""SELECT DISTINCT battery.userhash,battery.level,battery.timestamp FROM battery,(select userhash,count(distinct level) as countlevel from (SELECT * FROM battery WHERE timestamp >= """ + "'"+ str(dt) +"'"+ """) B group by userhash order by countlevel desc limit 3) AA WHERE AA.userhash = battery.userhash AND battery.timestamp >= """ + "'" + str(dt) + "'" + """ ORDER BY battery.userhash,battery.timestamp """)
        rows = self.my_cursor.fetchall()
        print(len(rows))
        data_final = {}


        

        for r in rows:

            if len(r)>=3 :

                level_value_for_user = []
                level_value_for_timestamp = []

                userhash_temp = r[0]
                level_temp = r[1]
                timestamp_temp = r[2]

                if userhash_temp in data_final.keys():
                    level_value_for_user = data_final[userhash_temp]["BatteryLevel"]
                    level_value_for_timestamp = data_final[userhash_temp]["BatteryTimeStamp"]
                    level_value_for_timestamp.append(timestamp_temp)
                    level_value_for_user.append(level_temp)
                else:
                    level_value_for_timestamp.append(timestamp_temp)
                    level_value_for_user.append(level_temp)

                data_final[userhash_temp] = { "BatteryLevel": level_value_for_user,"BatteryTimeStamp" : level_value_for_timestamp }
                #data_final[userhash_temp] = { "BatteryTimeStamp" : level_value_for_timestamp }
                    
        return data_final 

	#Get Battery Info Of All User For Last As Per Location 
    def getBatteryInforForAllUsersAsPerLocation(self,latitude_temp,longitude_temp,threshold_value,till_date=5):
        dt = datetime.datetime.today() - datetime.timedelta(till_date)
        dt = dt.timestamp()
        # self.my_cursor.execute("""select userhash,longitude,latitude,timestamp from location where userhash="""+"'"+(userhash)+"'"+"""and timestamp >= """+"'"+str(dt) +"'")
        self.my_cursor.execute(""" SELECT DISTINCT battery.userhash,battery.level,battery.timestamp FROM battery where userhash IN (select userhash from location where longitude <= cast (""" + str(longitude_temp + threshold_value) + """ as text) AND longitude >= cast( """ + str(longitude_temp - threshold_value) + """ as text) AND latitude <= cast ( """ + str(latitude_temp + threshold_value) + """ as text) AND latitude >= cast( """ + str(latitude_temp - threshold_value) + """ as text) AND timestamp >= """ + "'" + str(dt) + "'" + """ ) AND battery.timestamp >= """ + "'" + str(dt) + "'")
        rows = self.my_cursor.fetchall()
        # print(rows)
        data_final = {}


        

        for r in rows:

            if len(r)>=3 :

                level_value_for_user = []
                level_value_for_timestamp = []

                userhash_temp = r[0]
                level_temp = r[1]
                timestamp_temp = r[2]

                if userhash_temp in data_final.keys():
                    level_value_for_user = data_final[userhash_temp]["BatteryLevel"]
                    level_value_for_timestamp = data_final[userhash_temp]["BatteryTimeStamp"]
                    level_value_for_timestamp.append(timestamp_temp)
                    level_value_for_user.append(level_temp)
                else:
                    level_value_for_timestamp.append(timestamp_temp)
                    level_value_for_user.append(level_temp)

                data_final[userhash_temp] = { "BatteryLevel": level_value_for_user,"BatteryTimeStamp" : level_value_for_timestamp }
                #data_final[userhash_temp] = { "BatteryTimeStamp" : level_value_for_timestamp }
                    
        return data_final 

    def close_conn_cursor(self):
        self.my_cursor.close()
        self.conn.close()



if __name__ == "__main__":
    print("AAAAA")
    dbInstance = Database("127.0.0.1",'mydb3','postgres','qwerty')
    # print(dbInstance.getWifiDataForPresentation())
    # print(dbInstance.getBatteryInforForAllUsers())
    print(dbInstance.getBatteryInforForAllUsersAsPerLocation(17.445437,78.3456945,0.0035))
	# InvokeDBFunc()
    # print(dbInstance.probe_info())
