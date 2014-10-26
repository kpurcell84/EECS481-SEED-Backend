"""
Fetches patient data from Basis Health Tracker and stores it into database
"""

import webapp2
import urllib
import Cookie
import json
import time

from google.appengine.api import urlfetch
from google.appengine.ext import db
from models import *
from datetime import datetime, timedelta

class Fetch(webapp2.RequestHandler):
    username = 'seedsystem00@gmail.com'
    password = 'eecs481seed'
    export_date = '2014-10-24'
    export_offset = 0

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'

        self.cur_epoch = time.time()
        self.export_date = time.strftime(
            "%Y-%m-%d",
            time.localtime(self.cur_epoch))

        all_patients = Patient.all()
        all_patients.filter(
            '__key__ =', 
            Key.from_path('Patient', 'jinseok@umich.edu'))
        patient = all_patients.get()
        self.login()
        data = self.get_metrics(patient)
        self.store_data(patient, data)

    def login(self):
        """
        Login into Basis server
        Returns:
            True at success, False otherwise
        """
        url = 'https://app.mybasis.com/login'
        form_fields = {
            'username': self.username,
            'password': self.password,
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
        result = urlfetch.fetch(
            url=url,
            method=urlfetch.GET,
            headers={'Cookie': self.cookie_header},
            follow_redirects=False)
        decoded = json.loads(result.content)
        return decoded

    def get_metrics(self, patient):
        """
        Get patient data in JSON format

        Args:
            metrics_type 
                0 - ordinary metrics
                1 - sleep metrics
                2 - run, walk, bike metrics
        Returns:
            JSON string of patient data
        """

        metrics = {} 
        metrics['time'] = datetime.fromtimestamp(self.cur_epoch)
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
        index = int((self.cur_epoch - data['starttime'])/60 - 1)
        if index < 0:
            return metrics

        metrics['air_temp'] = data['metrics']['air_temp']['values'][index]
        metrics['gsr'] = data['metrics']['gsr']['values'][index]
        metrics['heart_rate'] = data['metrics']['heartrate']['values'][index]
        metrics['skin_temp'] = data['metrics']['skin_temp']['values'][index]

        self.export_date = '2014-10-08'
        url = 'https://app.mybasis.com/api/v2/users/me/days/' \
            + self.export_date + '/activities?' \
            + 'type=sleep' \
            + '&expand=activities.stages,activities.events'
        data = self.fetch_url(url)

        url = 'https://app.mybasis.com/api/v2/users/me/days/' \
            + self.export_date + '/activities?' \
            + 'type=run,walk,bike' \
            + '&expand=activities'
        data = self.fetch_url(url)

        metrics['activity'] = None
        metrics['toss_or_turn'] = None

        return metrics

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
                        activity_type=metrics['activity'],
                        toss_or_turn=metrics['toss_or_turn'])
            data.put()
            self.response.write("Success")
            return True

APPLICATION = webapp2.WSGIApplication([
    ('/cron/fetch', Fetch),
], debug=True)