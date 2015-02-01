import tornado.ioloop
import tornado.web
import socket
import sys
import json
from main import *

class MainHandler(tornado.web.RequestHandler):
	def prepare(self):
    		if self.request.headers["Content-Type"].startswith("text/plain"):
			print self.request.body
    		else:
        		print "Error"

if __name__ == "__main__":
	application = tornado.web.Application([
(r"/", MainHandler),
])
	application.listen(9999)
	tornado.ioloop.IOLoop.instance().start()
