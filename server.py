#!/bin/env python
# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
from tornado import gen
from fmww import ImageBot

class ContentHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	@gen.engine
	def get(self):
		code = self.get_argument('code')
		img_type = self.get_argument('type')

		binary = yield gen.Task(self.fetch_image, code)

		self.set_header("Content-type",  "image/jpeg")
		self.write(binary)
		self.finish()

	def fetch_image(self, code, callback):
		bot = ImageBot()
		binary = bot.get_image(code)
		callback(binary)

application = tornado.web.Application([
	(r"/imgbot", ContentHandler)
])

if __name__ == "__main__":
	application.listen(8888)
	tornado.ioloop.IOLoop.instance().start()
