import webapp2
from numpy import *
from google.appengine.ext import db
from models import *

class Train(webapp2.RequestHandler):
    eta = 0.0001
    c = 1
    num_features = 4
    w = zeros(num_features)

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.load_data()

    def load_data(self):
        self.response.write('Loading data...\n')
        data = {}
        all_patients = Patient.all()
        all_patients.filter('diagnosis !=', 'Maybe')
        for patient in all_patients:
            self.response.write(patient.first_name + '\n')
            all_quant_data = PQuantData.all()
            all_quant_data.filter('patient =', patient)
            all_quant_data.order('time_taken')
            for quant_data in all_quant_data:
                self.response.write('  ' + quant_data.time_taken.strftime("%Y-%m-%d %H:%M:%S") + '\n')

    #def get_feature_matrix(self, data):

    #def train(self):

APPLICATION = webapp2.WSGIApplication([
    ('/cron/train', Train),
], debug=True)