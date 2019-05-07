import json
from pprint import pprint
import re
import database as db
import shutil
import os
import datetime

class BusinessLayer:


	connection = None

	def __init__(self):
		self.connection = None	

	def CreateConnection(self):
		if self.connection == None:
			self.connection = db.Database('127.0.0.1','python_mysql','postgres','test')
	
	def getProbeInfo(self,userhash):
		self.CreateConnection()
		x = self.connection.probe_info(userhash)
		#print(x)
		self.connection.close_conn_cursor()
		self.connection = None
		return x

	def getBatteryInfoForAllUser(self):
		self.CreateConnection()
		x = self.connection.getBatteryInforForAllUsers()
		#print(x)
		self.connection.close_conn_cursor()
		self.connection = None
		return x
	
	def getBatteryInfoForAllUserAsPerLocation(self,latitude_temp,longitude_temp,threshold_value):
		self.CreateConnection()
		x = self.connection.getBatteryInforForAllUsersAsPerLocation(latitude_temp,longitude_temp,threshold_value)
		#print(x)
		self.connection.close_conn_cursor()
		self.connection = None
		return x

	def getAllUserHash(self):
		self.CreateConnection()
		x = self.connection.getAllUserHash()
		#print(x)
		self.connection.close_conn_cursor()
		return x

	def get_location_details_for_user(self,userhash,till_date=1):
		self.CreateConnection()
		x = self.connection.get_location_details_for_user(userhash,till_date)
		self.connection.close_conn_cursor()
		self.connection = None
		return x

	def get_wifi_details_for_user(self,userhash,till_date=1):
		self.CreateConnection()
		x = self.connection.get_wifi_details_for_user(userhash,till_date)
		self.connection.close_conn_cursor()
		self.connection = None
		return x

	def get_callstate_details_for_user(self,userhash,till_date=1):
		self.CreateConnection()
		x = self.connection.get_callstate_details_for_user(userhash,till_date)
		call_state_types_lower = ["idle","off-hook","ringing"]
		x_keys = list(x.keys())
		# print(type(x_keys))
		x_keys = [ittt.lower() for ittt in x_keys]
		for item in call_state_types_lower:
			if item not in x_keys:
				x[item] = 0

		self.connection.close_conn_cursor()
		self.connection = None
		return x

	def get_battery_details_for_user(self,userhash,till_date=1):
		self.CreateConnection()
		x = self.connection.get_battery_details_for_user(userhash,till_date)
		self.connection.close_conn_cursor()
		self.connection = None
		return x

	def getWifiDataForPresentation(self):
		self.CreateConnection()
		x = self.connection.getWifiDataForPresentation()
		self.connection.close_conn_cursor()
		self.connection = None
		return x
	
	def getNetworkDetailsForPresentation(self):
		self.CreateConnection()
		x = self.connection.getNetworkDetailsForPresentation()
		self.connection.close_conn_cursor()
		self.connection = None
		return x

if __name__ == "__main__":
	bobj = BusinessLayer()
	# print(bobj.getProbeInfo('34237272481aa6a02ea94799695a6982'))	
	print(bobj.getBatteryInfoForAllUser())
	# print(bobj.getWifiDataForPresentation())
	# print(bobj.getNetworkDetailsForPresentation())
	# print(bobj.get_wifi_details_for_user('34237272481aa6a02ea94799695a6982'))
	# print(bobj.get_battery_details_for_user('34237272481aa6a02ea94799695a6982'))
	# # print(bobj.get_callstate_details_for_user('34237272481aa6a02ea94799695a6982',2))
	# # print(bobj.get_location_details_for_user('34237272481aa6a02ea94799695a6982'))
