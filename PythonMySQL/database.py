import mysql.connector
from mysql.connector import Error
import psycopg2
from datetime import datetime

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
        print("---------------Object Creation IN DB ------------------------------")

    def probe_info(self):
        ret_dict = {}
        x1 = self.get_battery()
        uids = {}
        for r in x1:
            dt_object = datetime.fromtimestamp(int(r[2]))
            # dt_object = r[2]
            uids[r[0]] = [r[1],str(dt_object)]
        # print(r[0])
        ret_dict["battery"]=uids
        # print(uids)
        # print("----------------------------")
        x2 = self.get_callState()
        uids = {}
        for r in x2:
            dt_object = datetime.fromtimestamp(int(r[2]))
            uids[r[0]] = [r[1],str(dt_object)]
            # print(r[0])
        ret_dict["callstate"]=uids
        # print(uids)
        # print("----------------------------")
        x3 = self.get_location()
        uids = {}
        for r in x3:
            dt_object = datetime.fromtimestamp(int(r[3]))
            uids[r[0]] = [r[1],r[2],str(dt_object)]
            # print(r[0])
        ret_dict["location"]=uids
        # print(uids)
        return ret_dict

    
    def get_battery(self):
        self.my_cursor.execute("""select userhash,level,timestamp from battery order by timestamp""")
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

    # newobj.insert(k,col_str,s_str,tuple(record_list),myf)

    def insert(self,tname,col_str,s_str,record_list,myf):
        sql_insert_query = ""
        print("tname ----- IN DB ",tname)
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

    def close_conn_cursor(self):
        self.my_cursor.close()
        self.conn.close()

