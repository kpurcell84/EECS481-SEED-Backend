"""
Fetches patient data from Basis Health Tracker and stores it into database
"""

import webapp2
import urllib
import Cookie
import json
import time

from datetime import datetime, timedelta
from numpy import *
from math import *
from classification import *

from google.appengine.api import urlfetch
from google.appengine.ext import db
from models import *

class Fetch(webapp2.RequestHandler):
    patient_key = 'seedsystem00@gmail.com'
    export_offset = 0
    margin_of_error = 15 * 60 #in seconds

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'

        self.cur_epoch = time.time() - self.margin_of_error

        patient = Patient.get_patient(self.patient_key)
        username = patient.key().name()
        password = patient.basis_pass
        self.login(username, password)

        for i in range(30):
            self.cur_epoch -= 60
            self.export_date = time.strftime(
                "%Y-%m-%d",
                time.localtime(self.cur_epoch))
            data = self.get_metrics(patient)
            if data != None:
                self.response.write(data)
                self.response.write('\n')
                self.store_data(patient, data)
                self.check_data(patient, data)
                return

    def login(self, username, password):
        """
        Login into Basis server
        Returns:
            True at success, False otherwise
        """
        url = 'https://app.mybasis.com/login'
        form_fields = {
            'username': username,
            'password': password,
        }
        form_data = urllib.urlencode(form_fields)
        result = urlfetch.fetch(
            url=url,
            payload=form_data,
            method=urlfetch.POST,
            follow_redirects=False)
        cookie = Cookie.SimpleCookie()
        cookie.load(result.headers.get('set-cookie', ''))
        self.cookie_header = ''
        for value in cookie.values():
            self.cookie_header += '%s=%s; ' % (value.key, value.value)
        return True

    def fetch_url(self, url):
        """
        Fetch data from url in JSON format

        Args:
            url: URL string to fetch from
        Returns:
            decoded JSON object of data
        """
        result = urlfetch.fetch(
            url=url,
            method=urlfetch.GET,
            headers={'Cookie': self.cookie_header},
            follow_redirects=False)
        decoded = json.loads(result.content)
        return decoded

    def get_metrics(self, patient):
        """
        Get current patient quantitative data from Basis

        Args:
            patient: the corresponding Patient object of the fetched data
        Returns:
            Map of metrics types to values
        """

        metrics = {} 
        
        url = 'https://app.mybasis.com/api/v1/metricsday/me?' \
            + 'day=' + self.export_date \
            + '&padding=' + str(self.export_offset) \
            + '&heartrate=true' \
            + '&steps=true' \
            + '&calories=true' \
            + '&gsr=true' \
            + '&skin_temp=true' \
            + '&air_temp=true'
        data = self.fetch_url(url)
        index = int(self.cur_epoch - data['starttime'])/60

        metrics['air_temp'] = data['metrics']['air_temp']['values'][index]
        metrics['gsr'] = data['metrics']['gsr']['values'][index]
        metrics['heart_rate'] = data['metrics']['heartrate']['values'][index]
        metrics['skin_temp'] = data['metrics']['skin_temp']['values'][index]

        empty_data = False
        for key in metrics:
            if metrics[key] is None:
                empty_data = True

        metrics['time'] = datetime.fromtimestamp(self.cur_epoch)
        if empty_data:
            return None

        url = 'https://app.mybasis.com/api/v2/users/me/days/' \
            + self.export_date + '/activities?' \
            + 'type=sleep' \
            + '&expand=activities.stages,activities.events'
        data = self.fetch_url(url)

        is_active = False
        for activity in data['content']['activities']:
            for stage in activity['stages']:
                start_time = stage['start_time']['timestamp']
                end_time = stage['end_time']['timestamp']
                if self.cur_epoch >= start_time and self.cur_epoch <= end_time:
                    is_active = True
                    metrics['activity'] = stage['type'].title()

        if not is_active:
            url = 'https://app.mybasis.com/api/v2/users/me/days/' \
                + self.export_date + '/activities?' \
                + 'type=run,walk,bike' \
                + '&expand=activities'
            data = self.fetch_url(url)
            for activity in data['content']['activities']:
                start_time = activity['start_time']['timestamp']
                end_time = activity['end_time']['timestamp']
                if self.cur_epoch >= start_time and self.cur_epoch <= end_time:
                    is_active = True
                    metrics['activity'] = activity['type'].title()

        if not is_active:
            metrics['activity'] = 'Still'

        metrics['time'] = datetime.fromtimestamp(self.cur_epoch)
        return metrics

    def check_data(self, patient, metrics):
        """
        Checks if the fetched metrics indicates sepsis and triggers
        appropriate alerts

        Args:
            metrics: map of metrics type to values
        """
        weights = ClassWeights.get_recent_weights()
        manual_data = PQuantData.get_recent_manual_data(patient)
        qual_data = PQualData.get_recent_data(patient)
        if manual_data is None or qual_data is None or weights is None:
            return
        parsed_blood_pressure = manual_data.blood_pressure.split('/',1)
        systolic = float(parsed_blood_pressure[0])
        diastolic = float(parsed_blood_pressure[1])
        body_temp = manual_data.body_temp
        
        if metrics['activity'] == 'Run' or metrics['activity'] == 'Bike':
            features = matrix([[
                systolic,
                diastolic,
                body_temp,
                0.0,
                metrics['gsr'],
                0.0,
                quant_data.skin_temp,
                0.0,
                metrics['heart_rate'],
                0.0,
                qual_data
            ]])
        elif metrics['activity'] == 'Rem' or metrics['activity'] == 'Light' or metrics['activity'] == 'Deep':
            features = matrix([[
                systolic,
                diastolic,
                body_temp,
                metrics['gsr'],
                0.0,
                metrics['skin_temp'],
                0.0,
                0.0,
                0.0,
                metrics['heart_rate'],
                qual_data
            ]])
        else:
            features = matrix([[
                systolic,
                diastolic,
                body_temp,
                metrics['gsr'],
                0.0,
                metrics['skin_temp'],
                0.0,
                metrics['heart_rate'],
                0.0,
                0.0,
                qual_data
            ]])

        probability = classify(features, weights)

        self.response.write('Probability of having Sepsis: ')
        self.response.write(probability)
        self.response.write('\n')

        trigger_alert(patient.key().name(), probability)

        return

    def store_data(self, patient, metrics):
        """
        Store metrics into database

        Args:
            metrics: map of metrics type to values
        Returns:
            True on success, False otherwise
        """
        if patient == None:
            return False
        else:
            data = PQuantData(patient=patient,
                        time_taken=metrics['time'],
                        gsr=metrics['gsr'],
                        skin_temp=metrics['skin_temp'],
                        air_temp=metrics['air_temp'],
                        heart_rate=metrics['heart_rate'],
                        activity_type=metrics['activity'])
            data.put()
            return True

APPLICATION = webapp2.WSGIApplication([
    ('/cron/fetch', Fetch),
], debug=True)