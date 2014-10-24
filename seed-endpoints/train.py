import webapp2
import numpy

class Train(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!')

APPLICATION = webapp2.WSGIApplication([
    ('/cron/train', Train),
], debug=True)