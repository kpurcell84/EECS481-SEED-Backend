from google.appengine.ext import db
from models import *

from numpy import *
from math import *

# Helper functions for classification algorithm

NUM_FEATURES = 10

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
        if quant_data.activity_type == None:
            continue

        if quant_data.activity_type == 'Run' or quant_data.activity_type == 'Bike':
            feature = matrix([[
                systolic,
                diastolic,
                body_temp,
                0,
                quant_data.gsr,
                0,
                quant_data.skin_temp,
                0,
                quant_data.heart_rate,
                0
            ]])
        elif quant_data.activity_type == 'Rem' or quant_data.activity_type == 'Light' or quant_data.activity_type == 'Deep':
            feature = matrix([[
                systolic,
                diastolic,
                body_temp,
                quant_data.gsr,
                0,
                quant_data.skin_temp,
                0,
                0,
                0,
                quant_data.heart_rate
            ]])
        else:
            feature = matrix([[
                systolic,
                diastolic,
                body_temp,
                quant_data.gsr,
                0,
                quant_data.skin_temp,
                0,
                quant_data.heart_rate,
                0,
                0
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
    average_prob = 0
    for y in nditer(y_vector, op_flags=['readwrite']):
        average_prob += sigmoid(y)
        count += 1
        y[...] = sigmoid(y)
    average_prob /= count
    return y_vector
