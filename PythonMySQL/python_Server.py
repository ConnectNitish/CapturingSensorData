#!/usr/bin/env python

#import python_mysql_connect1 as ClassNeed
import os

"""
Very simple HTTP server in python.
Usage::
    ./dummy-web-server.py [<port>]
Send a GET request::
    curl http://localhost
Send a HEAD request::
    curl -I http://localhost
Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost
"""
# from http.server import BaseHTTPRequestHandler,HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
# import socketserver
import SocketServer
from json import loads
from dicttoxml import dicttoxml
#import Json2xml 

import datetime
import SaveData as saveDB

def timeStamped(fname, fmt='%Y-%m-%d-%H-%M-%S_{fname}'):
    return datetime.datetime.now().strftime(fmt).format(fname=fname)

class S(BaseHTTPRequestHandler):
	def _set_headers(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()

	def do_GET(self):
		#ClassNeed.connect(None)
		print("AAAAAAAAAAAAAAAAAAAAAAAA")
		#self._set_headers()
		#self.wfile.write("<html><body><h1>hi!</h1></body></html>")

	def do_HEAD(self):
		self._set_headers()

	def do_POST(self):
		# Doesn't do anything with posted data
		print("BBBBBBBBBBBBBBBBB")
		content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
		post_data = self.rfile.read(content_length) # <--- Gets the data itself
		#print(post_data) # <-- Print post data
		name_of_file = timeStamped('data_By_app.json')
		name_of_file_to_Store="Input_feed.json"

		exists = os.path.isfile(name_of_file_to_Store)	
		if exists:
			pass	

		#with open(timeStamped('data_By_app.json'),'w') as outf:
		#	outf.write(post_data)
		with open(name_of_file_to_Store,'w') as outf:
			outf.write(post_data)
			post_data = str(post_data)

		#SaveDataobj = saveDB.SaveData()
		#SaveDataobj.SaveDataToDB()


		#xml_data = dicttoxml(loads(post_data))
		#print(xml_data) # <-- Print post data

		#data = Json2xml.fromjsonfile(name_of_file).data 
		#data_object = Json2xml(data) 
		#data_object.json2xml()

		#with open(timeStamped(name_of_file+'.xml'),'w') as outf:
		#	outf.write(post_data)

		#self._set_headers()
		#ClassNeed.connect(post_data)
		self._set_headers()
		self.wfile.write("<html><body><h1>POST!</h1></body></html>")
        
def run(server_class=HTTPServer, handler_class=S, port=80):
    # server_address = ('192.168.122.1', port)
    # server_address = ('10.42.0.235', port)
    server_address = ('127.0.0.1', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
