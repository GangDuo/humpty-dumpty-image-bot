import ConfigParser
import urllib, urllib2
import requests

from HTMLParser import HTMLParser

class HTMLParserToSignIn(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.form = []

	def handle_starttag(self, tag, attrs):
		if tag.lower() == 'input':
			attribute_name = ''
			attribute_value = ''
			for i in attrs:
				if i[0].lower() == 'name':
					attribute_name = i[1]
				if i[0].lower() == 'value':
					attribute_value = i[1]
			if len(attribute_name) > 0:			
				self.form.append((attribute_name, attribute_value))

class ImageBot:
	def __init__(self):
		self.settings = ConfigParser.SafeConfigParser()
		self.settings.read('./.config')

	def get_image(self, code):
		base_url = 'https://' + self.settings.get('host', 'domain')
		parser = HTMLParserToSignIn()
		s = requests.Session()
		r = s.get(base_url + '/JMODE_ASP/faces/login.jsp')
		parser.feed(r.text)
		payload = {}
		settings = [self.settings.get('user', 'user'),
			        self.settings.get('user', 'person'),
			        self.settings.get('user', 'user_password'),
			        self.settings.get('user', 'person_password')]
		for i, val in enumerate(parser.form):
			if i < len(settings):
				payload[val[0]] = settings[i]
			else:
				payload[val[0]] = val[1]

		r = s.post(base_url + '/JMODE_ASP/faces/login.jsp', data = payload)
		r = s.get(base_url + '/JMODE_ASP/faces/contents/imageServlet?' + urllib.urlencode({"style": code, "id": 0, "dir": "system"}))
		return r.content
