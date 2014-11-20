import webapp2
from numpy import *
from math import *
from google.appengine.ext import db
from models import *

class Train(webapp2.RequestHandler):
    num_features = 6
    w_vector = zeros([num_features,1])
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

    tolerance = 0.0000001
    
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.load_data()
        self.train()
        #self.store_weights()

    def load_data(self):
        #self.response.write('Loading data...\n')
        data = []
        all_patients = Patient.all()
        all_patients.filter('diagnosis !=', 'Maybe')
        for patient in all_patients:
            #self.response.write(patient.first_name + '\n')
            if patient.diagnosis == 'Yes':
                t = matrix([[1.0]])
            else:
                t = matrix([[0.0]])
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

        #self.response.write(self.feature_matrix)
        #self.response.write(self.t_vector)

    def train(self):
        while True:
            y_vector = self.feature_matrix * self.w_vector
            for y in nditer(y_vector, op_flags=['readwrite']):
                y[...] = self.sigmoid(y)
            l_diff = transpose(self.feature_matrix) * (self.t_vector - y_vector)
            one_vector = ones(shape(y_vector))
            y_diag = diagflat(multiply(y_vector, y_vector - one_vector))
            hessian = transpose(self.feature_matrix) * y_diag * self.feature_matrix
            invHessian = linalg.inv(hessian)
            delta = invHessian * l_diff
            within_tolerance = True
            for i in nditer(delta):
                if fabs(i) > self.tolerance:
                    within_tolerance = False
                    break
            self.w_vector -= delta
            if within_tolerance:
                break;

        self.response.write(self.w_vector)

    def store_weights(self):
        """
        Store weights into datastore
        """
        data = ClassWeights(w1=self.w_vector[0,0],
                            w2=self.w_vector[1,0],
                            w3=self.w_vector[2,0],
                            w4=self.w_vector[3,0],
                            w5=self.w_vector[4,0],
                            w6=self.w_vector[5,0])
        db.put(data)

    def sigmoid(self, x):
        return 1 / (1 + exp(-x))



APPLICATION = webapp2.WSGIApplication([
    ('/cron/train', Train),
], debug=True)