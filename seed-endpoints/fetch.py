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


GCM_URL = 'https://android.googleapis.com/gcm/send'
API_KEY = 'AIzaSyASQHVSepuoISRArUhOXUrQIXHB6ZQzFRg'

class Fetch(webapp2.RequestHandler):
    patient_key = 'seedsystem00@gmail.com'
    export_offset = 0
    margin_of_error = 15 * 60 #in seconds
    mid_priority_threshold = 0.5
    high_priority_threshold = 0.75

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'

        self.cur_epoch = time.time() - self.margin_of_error

        patient = Patient.get_patient(self.patient_key)
        username = patient.key().name()
        password = patient.basis_pass
        self.login(username, password)

        for i in range(0,29):
            self.cur_epoch -= (i * 60)
            self.export_date = time.strftime(
                "%Y-%m-%d",
                time.localtime(self.cur_epoch))
            data = self.get_metrics(patient)
            if data != None:
                self.response.write(data)
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
        if manual_data == None:
            return
        parsed_blood_pressure = manual_data.blood_pressure.split('/',1)
        systolic = float(parsed_blood_pressure[0])
        diastolic = float(parsed_blood_pressure[1])
        
        if metrics['activity'] == 'Run' or metrics['activity'] == 'Bike':
            features = matrix([[
                systolic,
                diastolic,
                manual_data.body_temp,
                0,
                metrics['gsr'],
                0,
                quant_data.skin_temp,
                0,
                metrics['heart_rate'],
                0
            ]])
        elif metrics['activity'] == 'Rem' or metrics['activity'] == 'Light' or metrics['activity'] == 'Deep':
            features = matrix([[
                systolic,
                diastolic,
                manual_data.body_temp,
                metrics['gsr'],
                0,
                metrics['skin_temp'],
                0,
                0,
                0,
                metrics['heart_rate']
            ]])
        else:
            features = matrix([[
                systolic,
                diastolic,
                manual_data.body_temp,
                metrics['gsr'],
                0,
                metrics['skin_temp'],
                0,
                metrics['heart_rate'],
                0,
                0
            ]])

        probability = classify(features, weights)

        if probability < self.mid_priority_threshold:
            return

        doctor = patient.doctor
        
        if probability < self.high_priority_threshold:
            message = {
                'message': 'Patient "' \
                          + patient.first_name + ' ' \
                          + patient.last_name + ' shows some indications of sepsis.'
            }
        else:
            message = {
                'message': 'Your health data shows HIGH indications of sepsis. ' \
                         + 'Please contact doctor immediately.'
            }
            reg_ids = GcmCreds.get_reg_ids(patient.key().name())
            self.trigger_alert(reg_ids, message)
            message = {
                'message': 'Patient "' \
                          + patient.first_name + ' ' \
                          + patient.last_name + ' shows HIGH indications of sepsis.'
            }
        reg_ids = GcmCreds.get_reg_ids(doctor.key().name())
        self.trigger_alert(reg_ids, message)

        #reg_ids.append("APA91bHJ952iglrH8_cGY0OHu4UfA1DosW2o9ZwXT8Ki8YnHmpr5Y7SoRnwRgJZ3RCn37j_Fw3QbyHQYFmbatHqVgPi7mlO0m1JyExwXglgBW8H1mbeJmKF6KjwCwTvbse4NoyP8gGQI29zGy_Vk7Y9VQd6dPYj5ogcdETGYh4UYBFBWuWgWKwA")

        return

    def trigger_alert(self, reg_ids, data):
        """
        Triggers alert to doctor and optionally to patient

        Args:
            reg_ids: Array of device tokens to send alerts to
        """
        headers = {
            'Authorization': 'key=%s' % API_KEY,
            'Content-Type': 'application/json'
        }
        payload = {
            'registration_ids': reg_ids,
            'data': data
        }
        payload = json.dumps(payload)
        result = urlfetch.fetch(
            url=GCM_URL,
            method=urlfetch.POST,
            payload= payload,
            headers=headers,
            follow_redirects=False)
        if result.status_code == 200:
            decoded = json.loads(result.content)
            self.response.write("Request successfully transferred\n")
            self.response.write(decoded)
        elif result.status_code == 400:
            self.response.write("The request could not be parsed as JSON\n")
        elif result.status_code == 401:
            self.response.write("There was an error authenticating the sender account\n")
        elif result.status_code == 503:
            self.response.write("GCM service is unavailable\n")
        else:
            self.response.write("GCM service error: %d\n" % result.status_code)
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
            self.response.write("Success\n")
            return True

APPLICATION = webapp2.WSGIApplication([
    ('/cron/fetch', Fetch),
], debug=True)