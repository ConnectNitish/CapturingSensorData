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
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
#from json import loads
#from dicttoxml import dicttoxml
#import Json2xml 

import datetime
#import SaveData as saveDB

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

    def do_HEAD(self):
        self._set_headers()
    '''    
    def do_POST(self):
	# Doesn't do anything with posted data
	#print("BBBBBBBBBBBBBBBBB")
	content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
	post_data = self.rfile.read(content_length) # <--- Gets the data itself
	print(post_data) # <-- Print post data
	self._set_headers()
	self.wfile.write("<html><body><h1>POST!</h1></body></html>")
    '''   
def run(server_class=HTTPServer, handler_class=S, port=5543):
    server_address = ('10.4.20.64', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
