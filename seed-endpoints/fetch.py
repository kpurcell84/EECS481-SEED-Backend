import webapp2
import urllib
import Cookie
import json

from google.appengine.api import urlfetch

class Fetch(webapp2.RequestHandler):
	username = 'seedsystem00@gmail.com'
	password = 'eecs481seed'
	export_format = 'json'
	export_date = '2014-10-08'
	export_offset = 0

	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		self.cookie = Cookie.SimpleCookie()
		self.login()
		self.get_metrics(1);

	def make_cookie_header(self):
		cookie_header = ''
		for value in self.cookie.values():
			cookie_header += '%s=%s; ' % (value.key, value.value)
		return cookie_header

	def login(self):
		url = 'https://app.mybasis.com/login'
		form_fields = {
			'username': self.username,
			'password': self.password,
		}
		form_data = urllib.urlencode(form_fields)
		result = urlfetch.fetch(
			url=url,
			payload=form_data,
			method=urlfetch.POST,
			follow_redirects=False)
		self.cookie.load(result.headers.get('set-cookie', ''))

	def get_metrics(self, metrics_type):
		url = ''
		if metrics_type == 0:
			url = 'https://app.mybasis.com/api/v1/metricsday/me?' \
				+ 'day=' + self.export_date \
				+ '&padding=' + str(self.export_offset) \
				+ '&heartrate=true' \
				+ '&steps=true' \
				+ '&calories=true' \
				+ '&gsr=true' \
				+ '&skin_temp=true' \
				+ '&air_temp=true'
		elif metrics_type == 1:
			url = 'https://app.mybasis.com/api/v2/users/me/days/' \
				+ self.export_date + '/activities?' \
				+ 'type=sleep' \
				+ '&expand=activities.stages,activities.events'
		else:
			url = 'https://app.mybasis.com/api/v2/users/me/days/' \
				+ self.export_date + '/activities?' \
				+ 'type=run,walk,bike' \
				+ '&expand=activities'

		result = urlfetch.fetch(
			url=url,
			method=urlfetch.GET,
			headers={'Cookie': self.make_cookie_header()},
			follow_redirects=False)
		self.response.write(result.content)

APPLICATION = webapp2.WSGIApplication([
	('/cron/fetch', Fetch),
], debug=True)