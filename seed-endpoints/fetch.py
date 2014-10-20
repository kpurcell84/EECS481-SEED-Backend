import webapp2

class Fetch(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!')

APPLICATION = webapp2.WSGIApplication([
    ('/cron/fetch', Fetch),
], debug=True)