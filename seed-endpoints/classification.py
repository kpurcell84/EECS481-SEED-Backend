import json
import time

from datetime import datetime, timedelta

from google.appengine.api import urlfetch
from google.appengine.ext import db
from models import *

from numpy import *
from math import *

# Helper functions for classification algorithm
GCM_URL = 'https://android.googleapis.com/gcm/send'
API_KEY = 'AIzaSyASQHVSepuoISRArUhOXUrQIXHB6ZQzFRg'

EARLY_THRESHOLD = 0.5
EMERG_THRESHOLD = 0.75

NUM_FEATURES = 11
"""
Features:
    Systolic blood pressure
    Diastolic blood pressure
    Body temperature
    GSR (When inactive)
    GSR (When active)
    Skin temperature (When inactive)
    Skin temperature (When active)
    Heart rate (When inactive)
    Heart rate (When active)
    Heart rate (When sleep)
    Qualitative data yes ratio
"""

def sigmoid(x):
    """
    Computes sigmoid of x

    Returns:
        Sigmoid of x
    """
    return 1 / (1 + exp(-x))

def get_feature_matrix(patient):
    """
    Creates feature_matrix of patient 

    Args:
        patient: A Patient entity 
    Returns:
        Feature matrix of patient
    """
    feature_matrix = empty([0, NUM_FEATURES])
    all_quant_data = PQuantData.get_patient_data(patient)
    all_qual_data = PQualData.get_patient_data(patient)
    index_qual = 0

    if all_quant_data is None or all_quant_data is None:
        return None

    # Look for first logged data of blood pressure and body temperature
    contain_blood_pressure = False
    contain_body_temp = False
    for quant_data in all_quant_data:
        if quant_data.blood_pressure != None and not contain_blood_pressure:
            parsed_blood_pressure = quant_data.blood_pressure.split('/',1)
            systolic = float(parsed_blood_pressure[0])
            diastolic = float(parsed_blood_pressure[1])
            contain_blood_pressure = True
        if quant_data.body_temp != None and not contain_body_temp:
            body_temp = quant_data.body_temp
            contain_body_temp = True
        if contain_blood_pressure and contain_body_temp:
            break
    if not contain_blood_pressure or not contain_body_temp:
        return None

    # Create feature matrix
    for quant_data in all_quant_data:
        if quant_data.blood_pressure != None:
            parsed_blood_pressure = quant_data.blood_pressure.split('/',1)
            systolic = float(parsed_blood_pressure[0])
            diastolic = float(parsed_blood_pressure[1])
        if quant_data.body_temp != None:
            body_temp = quant_data.body_temp
        if quant_data.activity_type == None or \
                quant_data.gsr == None or \
                quant_data.skin_temp == None or \
                quant_data.heart_rate == None:
            continue

        if all_qual_data[index_qual].time_taken < quant_data.time_taken:
            if index_qual + 1 < len(all_qual_data):
                index_qual += 1

        # Calculate proportion of qual_data answered "Yes"
        qual_data = all_qual_data[index_qual]
        num_yes = 0.0
        if qual_data.a1 == "Yes":
            num_yes += 1.0
        if qual_data.a2 == "Yes":
            num_yes += 1.0
        if qual_data.a3 == "Yes":
            num_yes += 1.0
        if qual_data.a4 == "Yes":
            num_yes += 1.0
        if qual_data.a5 == "Yes":
            num_yes += 1.0
        if qual_data.a6 == "Yes":
            num_yes += 1.0
        if qual_data.a7 == "Yes":
            num_yes += 1.0
        if qual_data.a8 == "Yes":
            num_yes += 1.0
        if qual_data.a9 == "Yes":
            num_yes += 1.0
        if qual_data.a10 == "Yes":
            num_yes += 1.0
        p_yes = num_yes/10.0

        if quant_data.activity_type == 'Run' or quant_data.activity_type == 'Bike':
            feature = matrix([[
                systolic,
                diastolic,
                body_temp,
                0.0,
                quant_data.gsr,
                0.0,
                quant_data.skin_temp,
                0.0,
                quant_data.heart_rate,
                0.0,
                p_yes
            ]])
        elif quant_data.activity_type == 'Rem' or quant_data.activity_type == 'Light' or quant_data.activity_type == 'Deep':
            feature = matrix([[
                systolic,
                diastolic,
                body_temp,
                quant_data.gsr,
                0.0,
                quant_data.skin_temp,
                0.0,
                0.0,
                0.0,
                quant_data.heart_rate,
                p_yes
            ]])
        else:
            feature = matrix([[
                systolic,
                diastolic,
                body_temp,
                quant_data.gsr,
                0.0,
                quant_data.skin_temp,
                0.0,
                quant_data.heart_rate,
                0.0,
                0.0,
                p_yes
            ]])
        feature_matrix = append(feature_matrix, feature, axis=0)
    return feature_matrix

def classify(feature_matrix, w_vector):
    """
    Classifies whether input data indicates sepsis

    Args:
        feature_matrix: Feature matrix
    Returns:
        Average probability of having sepsis
    """
    y_vector = feature_matrix * w_vector
    count = 0
    average_prob = 0.0
    for y in nditer(y_vector, op_flags=['readwrite']):
        average_prob += sigmoid(y)
        count += 1
        y[...] = sigmoid(y)
    average_prob /= count
    return average_prob

def trigger_alert(email, probability):
    if probability < EARLY_THRESHOLD:
        return

    patient = Patient.get_patient(email)
    doctor = patient.doctor

    patient_name = patient.first_name + ' ' + patient.last_name

    data = {
        'patient_email': email,
        'patient_name': patient_name
    }

    if probability < EMERG_THRESHOLD:
        priority = 'Early'
        alert = Alert(patient=patient,
                    time_alerted=datetime.fromtimestamp(time.time()),
                    priority=priority)
        alert.put()
        data['priority'] = priority

    else:
        priority = 'Emergency'
        alert = Alert(patient=patient,
                    time_alerted=datetime.fromtimestamp(time.time()),
                    priority=priority)
        alert.put()
        data['priority'] = priority
        reg_ids = GcmCreds.get_reg_ids(email)
        send_alert(reg_ids, data)

    reg_ids = GcmCreds.get_reg_ids(doctor.key().name())
    send_alert(reg_ids, data)
    return

def send_alert(reg_ids, data):
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
        return decoded
    elif result.status_code == 400:
        msg = "The request could not be parsed as JSON\n"
    elif result.status_code == 401:
        msg = "There was an error authenticating the sender account\n"
    elif result.status_code == 503:
        msg = "GCM service is unavailable\n"
    else:
        msg = "GCM service error: %d\n" % result.status_code
    return
