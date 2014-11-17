import webapp2
from numpy import *
from google.appengine.ext import db
from models import *

class Train(webapp2.RequestHandler):
    eta = 0.0001
    c = 1
    num_features = 6
    w_vector = zeros(num_features)
    t_vector = empty([0,1])
    feature_matrix = empty([0, num_features])
    """
    Features:
        Systolic blood pressure
        Diastolic blood pressure
        Body temperature
        GSR
        Skin temperature
        Heart rate
    """
    
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.load_data()

    def load_data(self):
        self.response.write('Loading data...\n')
        data = []
        all_patients = Patient.all()
        all_patients.filter('diagnosis !=', 'Maybe')
        for patient in all_patients:
            self.response.write(patient.first_name + '\n')
            if patient.diagnosis == 'Yes':
                t = matrix([[1.0]])
            else:
                t = matrix([[-1.0]])
            all_quant_data = PQuantData.all()
            all_quant_data.filter('patient =', patient)
            all_quant_data.order('time_taken')
            for quant_data in all_quant_data:
                parsed_heart_rate = quant_data.blood_pressure.split('/',1)
                systolic = float(parsed_heart_rate[0])
                diastolic = float(parsed_heart_rate[1])
                features = matrix([[
                    systolic,
                    diastolic,
                    quant_data.body_temp,
                    quant_data.gsr,
                    quant_data.skin_temp,
                    quant_data.heart_rate
                ]])
                self.feature_matrix = append(self.feature_matrix, features, axis=0)
                self.t_vector = append(self.t_vector, t, axis=0)

        self.response.write(self.feature_matrix)
        self.response.write(self.t_vector)

    #def train(self):

APPLICATION = webapp2.WSGIApplication([
    ('/cron/train', Train),
], debug=True)