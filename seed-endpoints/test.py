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

        message = {
            'message': 'Your health data shows HIGH indications of sepsis. ' \
                     + 'Please contact doctor immediately.'
        }
        reg_ids = []
        reg_ids.append("APA91bHJ952iglrH8_cGY0OHu4UfA1DosW2o9ZwXT8Ki8YnHmpr5Y7SoRnwRgJZ3RCn37j_Fw3QbyHQYFmbatHqVgPi7mlO0m1JyExwXglgBW8H1mbeJmKF6KjwCwTvbse4NoyP8gGQI29zGy_Vk7Y9VQd6dPYj5ogcdETGYh4UYBFBWuWgWKwA")
        trigger_alert(reg_ids, message)


APPLICATION = webapp2.WSGIApplication([
    ('/test', Test),
], debug=True)