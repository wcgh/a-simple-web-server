# -*- coding: utf-8 -*-
import BaseHTTPServer
import os
class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
        Page = '''\
    <html>
    <body><p>this is a hello word page!
    <body>
    </body>
    </html>
    '''
        Error_Page='''\
    <html>
    <body>
    <h1>no such a path :{path}</h1>
    <p>{msg}</p>
    </body>
    </html>
    '''

        def do_GET(self):
	    self.full_path = os.getcwd() + self.path
	    try:
		if self.path=='/':
		    self.wfile.write(self.Page)
		else:
		    with open(self.full_path, "rb") as reader:
		        content = reader.read()
			self.send_content(content)
	    except IOError as msg:
		msg = "'{0}' can't be read: {1}".format(self.path, msg)
		self.handle_error(msg)



	def handle_error(self, msg):
	    content = self.Error_Page.format(path=self.path, msg=msg)
	    self.send_content(content)


	def send_content(self, content):
	    self.send_response(200)
	    self.send_header("Content-type", "text/html")
	    self.send_header("Content-Length", str(len(content)))
	    self.end_headers()
	    self.wfile.write(content)
	
	
	def list_dir(self,  full_path):
	    try:
		entries = os.listdir(full_path)
		bullets = ['<li>{0}</li>'.format(e) for e in entries if not e.startswith('.')]
		page = self.Listing_Page.format('\n'.join(bullets))
		self.send_content(page)
	    except OSError as msg:
		msg = "'{0}' can't be listed: {1}".format(self.path, msg)


if __name__=='__main__':
    serverAddress=('',8000)
    server=BaseHTTPServer.HTTPServer(serverAddress,RequestHandler)
    server.serve_forever()
