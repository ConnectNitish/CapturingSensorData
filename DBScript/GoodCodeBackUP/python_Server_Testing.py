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
from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver

#from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
#import SocketServer

#from json import loads
#from dicttoxml import dicttoxml
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
	    self._set_headers()
	    self.wfile.write("<html><body><h1>hi!</h1></body></html>")

    def do_POST(self):
	    #ClassNeed.connect(None)
	    content_length = int(self.headers['Content-Length'])
	    post_data = self.rfile.read(content_length)
	    name_of_file = timeStamped('data_By_app.json')
	    name_of_file_to_Store="Input_feed.json"
	    exists = os.path.isfile(name_of_file_to_Store)

	    if exists == True:
	    	pass


	    with open(name_of_file_to_Store,'wb') as outf:
	    	outf.write(post_data)
	    post_data = str(post_data)
	    
	    SaveDataobj = saveDB.SaveData()
	    SaveDataobj.SaveDataToDB()


    def do_HEAD(self):
        self._set_headers()

"""        
    def do_POST(self):
		content_length = int(self.headers['Content-Length'])
		post_data = self.rfile.read(content_length)
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

		SaveDataobj = saveDB.SaveData()
		SaveDataobj.SaveDataToDB()
"""
       
def run(server_class=HTTPServer, handler_class=S, port=5543):
    server_address = ('0.0.0.0', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]),host="0.0.0.0")
    else:
        run()
