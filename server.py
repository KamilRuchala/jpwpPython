import tornado.ioloop
import tornado.web
import json
from main import *

class MainHandler(tornado.web.RequestHandler):
	def prepare(self):
    		if self.request.headers["Content-Type"].startswith("application/json"):
        		self.json_args = json.loads(self.request.body)
			#self.write(self.json_args)
    		else:
        		self.json_args = None
	def post(self):
		content = self.json_args['content']
		self.write(odpowiedz(content))

if __name__ == "__main__":
	application = tornado.web.Application([
(r"/", MainHandler),
])
	application.listen(8888)
	tornado.ioloop.IOLoop.instance().start()
