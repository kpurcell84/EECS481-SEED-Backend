from random import randrange, uniform
import time
from datetime import datetime, timedelta

from google.appengine.ext import db
from models import *
from sample_data import *

def generate_doctors():
    random_data = []

    for dic in doctor_list:
        new_doctor = Doctor(key_name=dic['email'],
                            first_name=dic['first_name'],
                            last_name=dic['last_name'],
                            phone=dic['phone'],
                            hospital=dic['hospital'])
        random_data.append(new_doctor)

    db.put(random_data)

def generate_patients():
    random_data = []

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
                              septic_risk=dic['septic_risk'],
                              basis_pass=dic['basis_pass'])
        random_data.append(new_patient)

    db.put(random_data)

# Each element in the pattern represents what range of vals to use for a timestamp
# 0 = Normal, No
# 1 = Medium, Maybe
# 2 = Sepsis, Yes
def get_pattern(patient, num_inserts):
    pattern = [0]*num_inserts # Pattern for vitals
    one_third = num_inserts/3
    two_thirds = (num_inserts*2)/3
    if patient.diagnosis == "Yes":
        pattern[one_third:two_thirds] = [1]*(two_thirds-one_third);
        pattern[two_thirds:] = [2]*(len(pattern)-two_thirds);
    elif patient.diagnosis == "Maybe":
        pattern[one_third:two_thirds] = [1]*(two_thirds-one_third);

    return pattern

def generate_quant_data():
    patient_list.pop() # Get rid of Andy

    random_data = []  
    for dic in patient_list:
        q = Patient.all()
        q.filter('__key__ =', Key.from_path('Patient', dic['email']))
        patient = q.get()
        if patient == None:
            continue

        fmt = '%Y-%m-%dT%H:%M:%S'
        start_time = datetime.strptime('2000-01-01T08:00:00', fmt)
        end_time = datetime.strptime('2000-01-04T08:00:00', fmt)

        # convert to unix timestamp
        d1_ts = time.mktime(start_time.timetuple())
        d2_ts = time.mktime(end_time.timetuple())

        # Frequency of entries in minutes
        frequency = 30

        timediff = int(d2_ts-d1_ts) / 60
        # Total number of entries per patient
        num_inserts = timediff / frequency

        pattern = get_pattern(patient, num_inserts)
        sp = 0
        s_idx = 0 # sleep index
        # Randomly generate values
        for i in range(num_inserts):
            time_taken = start_time + timedelta(minutes=i*frequency)
            p = pattern[i]

            blood_pressure = None
            body_temp = None
            # Only set manual metrics if time is 9am or 9pm
            if ((time_taken.hour == 9 or time_taken.hour == 21) and time_taken.minute == 0):
                sys_blood_pressure = randrange(sbp_low[p], sbp_high[p])
                dia_blood_pressure = randrange(dbp_low[p], dbp_high[p])
                blood_pressure = str(sys_blood_pressure) + "/" + str(dia_blood_pressure)

                body_temp = round(uniform(bt_low[p], bt_high[p]), 1)

            gsr = round(uniform(gsr_low[p], gsr_high[p]), 5)

            skin_temp = round(uniform(st_low[p], st_high[p]), 1)

            air_temp = round(uniform(at_low, at_high), 1)

            heart_rate = randrange(hr_low[p], hr_high[p])

            activity_type = None
            
            if (time_taken.hour == 0 and time_taken.minute == 0):
                # Set sleep pattern num to be average of pattern
                # nums over sleep interval
                sleep_pattern = pattern[i:i+9]
                avg = 0
                for j in sleep_pattern:
                    avg += (1.0/8.0)*j
                sp = int(round(avg, 0))
                s_idx = 0
            if (time_taken.hour >= 0 and time_taken.hour < 8):
                activity_type = sleep_list[sp][s_idx]
                s_idx += 1
                # Adjust heart rate to account for sleeping
                heart_rate -= 20
            else:
                activity_type = active_list[randrange(1,100)]
                if activity_type == 'Bike' or activity_type == 'Run':
                    # Adjust heart rate to account for being active
                    heart_rate += 50
                    gsr += 0.25
                    skin_temp += 10

            random_datum = PQuantData(patient=patient,
                                time_taken=time_taken,
                                blood_pressure=blood_pressure,
                                body_temp=body_temp,
                                gsr=gsr,
                                skin_temp=skin_temp,
                                air_temp=air_temp,
                                heart_rate=heart_rate,
                                activity_type=activity_type)
            random_data.append(random_datum)

    db.put(random_data)

def generate_qual_data():
    random_data = []

    for dic in patient_list:
        q = Patient.all()
        q.filter('__key__ =', Key.from_path('Patient', dic['email']))
        patient = q.get()
        if patient == None:
            continue

        fmt = '%Y-%m-%dT%H:%M:%S'
        start_time = datetime.strptime('2000-01-01T18:00:00', fmt)
        end_time = datetime.strptime('2000-01-04T18:00:00', fmt)

        # convert to unix timestamp
        d1_ts = time.mktime(start_time.timetuple())
        d2_ts = time.mktime(end_time.timetuple())

        frequency = 60 * 24

        timediff = int(d2_ts-d1_ts) / 60
        num_inserts = timediff / frequency

        pattern = get_pattern(patient, num_inserts)

        for i in range(num_inserts):
            time_taken = start_time + timedelta(minutes=i*frequency)
            vals = ["No"]*10
            if pattern[i] == 0:
                vals[0] = "Yes"
            elif pattern[i] == 1:
                vals[0:5] = ["Yes"]*5
            elif pattern[i] == 2:
                vals[1:10] = ["Yes"]*9

            a1 = vals[0]
            a2 = vals[1]
            a3 = vals[2]
            a4 = vals[3]
            a5 = vals[4]
            a6 = vals[5]
            a7 = vals[6]
            a8 = vals[7]
            a9 = vals[8]
            a10 = vals[9]

            random_datum = PQualData(patient=patient,
                                time_taken=time_taken,
                                a1=a1,a2=a2,
                                a3=a3,a4=a4,
                                a5=a5,a6=a6,
                                a7=a7,a8=a8,
                                a9=a9, a10=a10)
            random_data.append(random_datum)

    db.put(random_data)

def generate_alerts():
    random_data = []

    for dic in patient_list:
        q = Patient.all()
        q.filter('__key__ =', Key.from_path('Patient', dic['email']))
        patient = q.get()
        if patient == None:
            continue

        fmt = '%Y-%m-%dT%H:%M:%S'
        start_time = datetime.strptime('2000-01-01T08:00:00', fmt)
        end_time = datetime.strptime('2000-01-04T08:00:00', fmt)

        # convert to unix timestamp
        d1_ts = time.mktime(start_time.timetuple())
        d2_ts = time.mktime(end_time.timetuple())

        # Frequency of entries in minutes
        frequency = 30

        timediff = int(d2_ts-d1_ts) / 60
        # Total number of entries per patient
        num_inserts = timediff / frequency

        time_alerted = start_time
        
        pattern = get_pattern(patient, num_inserts)

        message_early = "You may be at risk of sepsis, please contact your doctor"
        message_emerg = "You are at serious risk of sepsis, please contact your doctor immediately"

        # Iteratate through pattern and find spots to trigger an alert
        # 4 consecutive maybe = early alert
        # 2 consecutive yes = emergency alert
        count1 = 0
        count2 = 0
        for i in range(num_inserts):
            time_alerted += timedelta(minutes=30)
            if pattern[i] == 0:
                count1 = 0
                count2 = 0
            elif pattern[i] == 1:
                count1 += 1
            elif pattern[i] == 2:
                count2 += 1

            if count1 == 8:
                alert = Alert(patient=patient,
                                 time_alerted=time_alerted,
                                 message=message_early,
                                 priority='Early')
                random_data.append(alert)
                count1 = 0
                count2 = 0
            elif count2 == 4:
                alert = Alert(patient=patient,
                                 time_alerted=time_alerted,
                                 message=message_emerg,
                                 priority='Emergency')
                random_data.append(alert)
                count1 = 0
                count2 = 0

    db.put(random_data)

def generate_watson_questions():
    random_data = []

    fmt = '%Y-%m-%dT%H:%M:%S'
    time_asked = datetime.strptime('2000-01-01T00:00:00', fmt) 
    for dic in watson_list:
        time_asked = time_asked + timedelta(hours=2)

        new_question = WatsonQuestion(question=dic['question'],
                                      answer=dic['answer'],
                                      time_asked=time_asked)

        random_data.append(new_question)

    db.put(random_data)

def generate_gcm_creds():
    pass

def generate_sample_data():
    # Must sleep between to make sure database updates
    print "Generating sample data"
    generate_doctors()
    time.sleep(2)
    generate_patients()
    time.sleep(2)
    generate_quant_data()
    generate_qual_data()
    generate_alerts()
    # generate_watson_questions()
    # generate_gcm_creds()