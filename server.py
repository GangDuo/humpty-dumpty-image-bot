#!/bin/env python
# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
from fmww import ImageBot

class ContentHandler(tornado.web.RequestHandler):
	def get(self):
		code = self.get_argument('code')
		img_type = self.get_argument('type')

		bot = ImageBot()
		binary = bot.get_image(code)

		self.set_header("Content-type",  "image/jpeg")
		self.write(binary)
		self.finish()

application = tornado.web.Application([
	(r"/imgbot", ContentHandler)
])

if __name__ == "__main__":
	application.listen(8888)
	tornado.ioloop.IOLoop.instance().start()
