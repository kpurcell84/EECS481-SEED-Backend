import random
from datetime import datetime, timedelta

from models import *
from sample_data import *

def generate_doctors():
    for dic in doctor_list:
        new_doctor = Doctor(key_name=dic['email'],
                            first_name=dic['first_name'],
                            last_name=dic['last_name'],
                            phone=dic['phone'],
                            hospital=dic['hospital'])
        new_doctor.put()

def generate_patients():
    for dic in patient_list:
        q = Doctor.all()
        q.filter('__key__ =', Key.from_path('Doctor', dic['doctor_email']))
        doctor = q.get()
        if doctor == None:
            continue

        new_patient = Patient(key_name=dic['email'],
                              doctor=doctor,
                              first_name=dic['first_name'],
                              last_name=dic['last_name'],
                              phone=dic['phone'],
                              diagnosis=dic['diagnosis'],
                              septic_risk=dic['septic_risk'])
        new_patient.put()

def generate_quant_data():
    q = Patient.all()
    q.filter('__key__ =', Key.from_path('Patient', message.email))
    patient = q.get()

    if patient == None:
        print "Cannot put random data, patient doesn't exist"
        return 

    timediff = message.end_time - message.start_time
    timediff = timediff.seconds / 60
    num_inserts = timediff / message.frequency

    for i in range(num_inserts):
        time_taken = message.start_time + timedelta(minutes=i*message.frequency)
        blood_pressure = str(random.randrange(80, 110))
        body_temp = float(random.randrange(97, 101))
        heart_rate = random.randrange(60, 150)

        random_pdata = cls(patient=patient,
                            time_taken=time_taken,
                            blood_pressure=blood_pressure,
                            body_temp=body_temp,
                            heart_rate=heart_rate)
        random_pdata.put()

    return

def generate_qual_data():
    pass

def generate_alerts():
    pass

def generate_watson_questions():
    pass

def generate_sample_data():
    print "Generating sample data"
    generate_doctors()
    generate_patients()
    # generate_quant_data()
    # generate_qual_data()
    # generate_alerts()
    # generate_watson_questions()