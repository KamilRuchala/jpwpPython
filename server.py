import tornado.ioloop
import tornado.web
import socket
import sys
import json
from main import *


sock = socket.socket(socket.AF_INET,                  socket.SOCK_DGRAM)

class MainHandler(tornado.web.RequestHandler):
	def prepare(self):
    		if self.request.headers["Content-Type"].startswith("application/json"):
			self.json_args = json.loads(self.request.body)
    		else:
        		self.json_args = None
	def post(self):
		content = self.json_args['content']
		PORT = int(self.json_args['port'])
		HOST = self.json_args['address']
		sock.sendto(odpowiedz(content), (HOST, PORT))
		#self.write(odpowiedz(content))

if __name__ == "__main__":
	application = tornado.web.Application([
(r"/", MainHandler),
])
	application.listen(8888)
	tornado.ioloop.IOLoop.instance().start()
