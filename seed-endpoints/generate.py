import random
from datetime import datetime, timedelta

from models import *

def generate_sample_data():
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