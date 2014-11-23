import webapp2

from numpy import *
from math import *

from google.appengine.ext import db
from models import *
from classification import *

class Test(webapp2.RequestHandler):
    """
    Script to test classification algorithm
    """
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'

        self.w_vector = ClassWeights.get_recent_weights()

        all_patients = Patient.all()
        self.response.write('Testing classificaton algorithm...\n')
        for p in all_patients:
            data = get_feature_matrix(p)
            if data is not None:
                prob = classify(data, self.w_vector)
                self.response.write(p.first_name + ' ' + p.last_name + ':\n')
                self.response.write(prob)
                self.response.write('\n')

APPLICATION = webapp2.WSGIApplication([
    ('/test', Test),
], debug=True)