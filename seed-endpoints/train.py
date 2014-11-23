import webapp2

import time
from datetime import datetime, timedelta

from google.appengine.ext import db
from models import *

from numpy import *
from math import *
from classification import *

class Train(webapp2.RequestHandler):
    w_vector = zeros([NUM_FEATURES,1])
    t_vector = empty([0,1])
    feature_matrix = empty([0, NUM_FEATURES])

    tolerance = 0.00000000001
    
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.load_data()
        self.train()
        self.store_weights()

    def load_data(self):
        data = []
        all_patients = Patient.all()
        all_patients.filter('diagnosis !=', 'Maybe')
        for patient in all_patients:
            feature = get_feature_matrix(patient)
            if feature is None:
                continue
            if patient.diagnosis == 'Yes':
                t = ones((feature.shape[0], 1))
            else:
                t = zeros((feature.shape[0], 1))

            self.feature_matrix = append(self.feature_matrix, feature, axis=0)
            self.t_vector = append(self.t_vector, t, axis=0)

        #self.response.write(self.feature_matrix)
        #self.response.write(self.t_vector)

    def train(self):
        count = 0
        while True:
            y_vector = self.feature_matrix * self.w_vector
            for y in nditer(y_vector, op_flags=['readwrite']):
                y[...] = sigmoid(y)
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
                break
        self.response.write(self.w_vector)

    def store_weights(self):
        """
        Store weights into datastore
        """
        self.cur_epoch = time.time()
        data = ClassWeights(time_taken=datetime.fromtimestamp(self.cur_epoch),
                            w1=float(self.w_vector[0,0]),
                            w2=float(self.w_vector[1,0]),
                            w3=float(self.w_vector[2,0]),
                            w4=float(self.w_vector[3,0]),
                            w5=float(self.w_vector[4,0]),
                            w6=float(self.w_vector[5,0]),
                            w7=float(self.w_vector[6,0]),
                            w8=float(self.w_vector[7,0]),
                            w9=float(self.w_vector[8,0]),
                            w10=float(self.w_vector[9,0]))
        data.put()

APPLICATION = webapp2.WSGIApplication([
    ('/cron/train', Train),
], debug=True)