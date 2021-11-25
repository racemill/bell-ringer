#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import ringUtils
import logging

homepagePath = "/usr/local/bell-ringer/index.html"
hostName = "192.168.50.6"
serverPort = 80
logging.basicConfig(filename='/var/log/bell.log', format=' %(message)s %(asctime)s', datefmt='%I:%M:%S %p %m/%d/%Y', level=logging.DEBUG)

class BellServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.handleHomepageRequest()
            return

        self.send_response(404)
           
    def do_POST(self):   # This is where you land when pressing the "RING THAT BELL" button on web page.
        if self.path == "/ring":
            logging.info("Web Ring Request from %s at         ", self.client_address[0])
            self.handleRingBellRequest();

    def handleHomepageRequest(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        content = open(homepagePath, 'rb').read()
        self.wfile.write(content)

    def handleRingBellRequest(self):
        ringResult = ringUtils.ringOnce()
        if ringResult == 403:       # Time Guard is On and not in allowed time range  
           self.send_response(403)
        elif ringResult == 429:     # Too soon after previous ring
           self.send_response(429)
        elif ringResult == 200:     # All good, worked.
           self.send_response(200)
        else:
           logging.info('No valid return from ringUtil ')
           self.send_response(404)
        self.send_header("Content-type", "text/html")
        self.end_headers()

def run_server():
    webServer = HTTPServer((hostName, serverPort), BellServer)
    print("Server started http://%s:%s" % (hostName, serverPort))
    logging.info('Server Started.................................')

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("  Server stopped.")
    logging.info('Server Stopped.................................')

if __name__ == "__main__":        
    ringUtils.initialize()
    try:
        run_server()
    finally:
        ringUtils.cleanup()

