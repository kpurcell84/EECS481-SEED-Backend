"""
Defines the models for the backend datastore
"""

from google.appengine.ext import endpoints
from google.appengine.ext import db

from google.appengine.api.datastore import Key

from messages import *

from numpy import *

class Doctor(db.Model):
    first_name = db.StringProperty(required=True)
    last_name = db.StringProperty(required=True)
    phone = db.PhoneNumberProperty(required=True)
    hospital = db.StringProperty()

    def to_message(self):
        """
        Turns the Doctor entity into a ProtoRPC object.
        """
        return DoctorPut(email=self.key().name(),
                                first_name=self.first_name,
                                last_name=self.last_name,
                                phone=self.phone,
                                hospital=self.hospital)

    def get_patients(self):
        """
        Builds a message consisting of all the doctor's patients
        Returns:
            An instance of PatientListResponse
        """
        patients = [patient.to_message() for patient in self.patient_set]
        return PatientListResponse(patients=patients)

    def get_alerts(self):
        """
        Builds a message consisting of all the doctor's patients alerts
        Returns:
            An instance of AlertListResponse
        """
        alerts = []
        for patient in self.patient_set:
            for alert in patient.alert_set:
                alerts.append(alert.to_message())    
        return AlertListResponse(alerts=alerts)

    @classmethod
    def put_from_message(cls, message):
        """
        Inserts a doctor into the DB

        Args:
            message: A DoctorPut instance to be inserted, note that the email is used as the entity key
        Returns:
            The Doctor entity that was inserted.
        """
        new_doctor = cls(key_name=message.email,
                        first_name=message.first_name,
                        last_name=message.last_name,
                        phone=message.phone,
                        hospital=message.hospital)
        new_doctor.put()
        return new_doctor


class Patient(db.Model):
    doctor = db.ReferenceProperty(Doctor, required=True)
    first_name = db.StringProperty(required=True)
    last_name = db.StringProperty(required=True)
    phone = db.PhoneNumberProperty(required=True)
    diagnosis = db.StringProperty(required=True) # Yes|No|Maybe
    septic_risk = db.IntegerProperty(required=True) # 1-99
    basis_pass = db.StringProperty(required=True)

    def to_message(self):
        """
        Turns the Patient entity into a ProtoRPC object.
        """
        return PatientPut(email=self.key().name(),
                            first_name=self.first_name,
                            last_name=self.last_name,
                            phone=self.phone,
                            doctor_email=self.doctor.key().name(),
                            diagnosis=self.diagnosis,
                            septic_risk=self.septic_risk,
                            basis_pass=self.basis_pass)

    @classmethod
    def put_from_message(cls, message):
        """
        Inserts a patient into the DB

        Args:
            message: A PatientPut instance to be inserted.
        Returns:
            The Patient entity that was inserted.
        """
        q = Doctor.all()
        q.filter('__key__ =', Key.from_path('Doctor', message.doctor_email))
        doctor = q.get()

        new_patient = cls(key_name=message.email,
                        doctor=doctor,
                        first_name=message.first_name,
                        last_name=message.last_name,
                        phone=message.phone,
                        diagnosis='No',
                        septic_risk=-1,
                        basis_pass=message.basis_pass)
        new_patient.put()
        return new_patient

    @classmethod
    def get_patient(cls, email):
        """
        Gets patient data

        Args:
            email: Patient e-mail address
        Returns:
            The Patient entity with corresponsing e-mail address
        """
        p = cls.all()
        p.filter('__key__ =', Key.from_path('Patient', email))
        return p.get()

class PQuantData(db.Model):
    patient = db.ReferenceProperty(Patient, required=True)
    time_taken = db.DateTimeProperty(required=True)
    blood_pressure = db.StringProperty()
    body_temp = db.FloatProperty() # Fahrenheit
    gsr = db.FloatProperty()
    skin_temp = db.FloatProperty() # Fahrenheit
    air_temp = db.FloatProperty() # Fahrenheit
    heart_rate = db.IntegerProperty()
    activity_type = db.StringProperty() # Still|Run|Bike|Walk|Rem|Light|Deep

    def to_message(self):
        """
        Turns the PQuantData entity into a ProtoRPC object.
        """
        return PQuantDataResponse(time_taken=self.time_taken,
                            blood_pressure=self.blood_pressure,
                            body_temp=self.body_temp,
                            gsr = self.gsr,
                            skin_temp = self.skin_temp,
                            air_temp = self.air_temp,
                            heart_rate = self.heart_rate,
                            activity_type = self.activity_type)

    @classmethod
    def get_range(cls, message, patient):
        """
        Builds a message consisting of all the available patient data within the requested time range
        Returns:
            An instance of PQuantDataListResponse
        """
        q = cls.all()
        q.filter('patient =', patient)
        q.filter('time_taken >=', message.start_time)
        q.filter('time_taken <=', message.end_time)
        q.order('time_taken')

        pdata_list = [ pdata.to_message() for pdata in q.run() ]

        return PQuantDataListResponse(pdata_list=pdata_list)

    @classmethod
    def get_patient_data(cls, patient):
        """
        Gets all quantitative data of specific patient in increasing time order

        Args:
            patient: A Patient entity
        Returns:
            A List of all quantitative data of patient
        """
        q = cls.all()
        q.filter('patient =', patient)
        q.order('time_taken')
        return q

    @classmethod
    def get_recent_manual_data(cls, patient):
        """
        Gets most recently logged blood pressure and heart rate

        Args:
            patient: A Patient entity
        Returns:
            A data point with most recent blood pressure and heart rate
        """
        q_all = cls.all()
        q_all.filter('patient =', patient)
        q_all.order('-time_taken')
        for q in q_all:
            if q.blood_pressure is not None:
                return q
        return None

class PQualData(db.Model):
    patient = db.ReferenceProperty(Patient, required=True)
    time_taken = db.DateTimeProperty(required=True)
    # Do you feel less energetic than usual?
    a1 = db.StringProperty(required=True) # Yes|No
    # Do you have any muscle aches?
    a2 = db.StringProperty(required=True) # Yes|No
    # Do you have abdominal pain?
    a3 = db.StringProperty(required=True) # Yes|No
    # Do you have a headache?
    a4 = db.StringProperty(required=True) # Yes|No
    # Do you feel you have to work hard to breathe?
    a5 = db.StringProperty(required=True) # Yes|No
    # Do you feel tightness in your lungs?
    a6 = db.StringProperty(required=True) # Yes|No
    # Do you have a cough?
    a7 = db.StringProperty(required=True) # Yes|No
    # Have you lost weight recently?
    a8 = db.StringProperty(required=True) # Yes|No
    # Is your urine output significantly lower than usual?
    a9 = db.StringProperty(required=True) # Yes|No
    # Do you feel down, depressed, or hopeless?
    a10 = db.StringProperty(required=True) # Yes|No

    def to_message(self):
        """
        Turns the PQualData entity into a ProtoRPC object.
        """
        return PManDataPut(email=self.patient.key().name(),
                            time_taken=self.time_taken,
                            a1=self.a1, a2=self.a2,
                            a3=self.a3, a4=self.a4,
                            a5=self.a5, a6=self.a6,
                            a7=self.a7, a8=self.a8,
                            a9=self.a9, a10=self.a10)

    @classmethod
    def get_range(cls, message, patient):
        """
        Builds a message consisting of all the available patient data within the requested time range
        Returns:
            An instance of PQualDataListResponse
        """
        q = cls.all()
        q.filter('patient =', patient)
        q.filter('time_taken >=', message.start_time)
        q.filter('time_taken <=', message.end_time)
        q.order('time_taken')

        pdata_list = [ pdata.to_message() for pdata in q.run() ]

        return PQualDataListResponse(pdata_list=pdata_list)

    @classmethod
    def put_from_message(cls, message, patient):
        """
        Inserts a piece of qualitative data from the survey in the db

        Args:
            message: A PQualDataPut instance to be inserted, note that the email is used as the entity key
        Returns:
            Nothing
        """
        new_datum = cls(patient=patient,
                        time_taken=message.time_taken,
                        a1=message.a1,
                        a2=message.a2,
                        a3=message.a3,
                        a4=message.a4,
                        a5=message.a5,
                        a6=message.a6,
                        a7=message.a7,
                        a8=message.a8,
                        a9=message.a9,
                        a10=message.a10)
        new_datum.put()
        return


class Alert(db.Model):
    patient = db.ReferenceProperty(Patient, required=True)
    time_alerted = db.DateTimeProperty(required=True)
    priority = db.StringProperty(required=True) # Early|Emergency

    def to_message(self):
        """
        Turns the Alert entity into a ProtoRPC object. 
        """
        return AlertResponse(patient_email=self.patient.key().name(),
                             time_alerted=self.time_alerted,
                             priority=self.priority)

    @classmethod
    def get_alerts(cls, message, user, u_type):
        """
        Builds a message consisting of all the alerts for a patient
        Returns:
            An instance of AlertListResponse
        """
        alerts = []

        q = cls.all()
        q.filter('time_alerted >=', message.start_time)
        q.filter('time_alerted <=', message.end_time)

        if u_type == "Patient":
            q.filter('patient =', user)
            q.filter('priority =', 'Emergency')
            alerts = [ alert.to_message() for alert in q.run() ]
        elif u_type == "Doctor":
            for patient in user.patient_set:
                for alert in patient.alert_set:
                    alerts.append(alert.to_message())
        q.order('-time_alerted')

        return AlertListResponse(alerts=alerts)


class WatsonQuestion(db.Model):
    question = db.StringProperty(required=True)
    answer = db.StringProperty(required=True)
    time_asked = db.DateTimeProperty(auto_now_add=True)

    def to_message(self):
        """
        Turns the WatsonQuestion entity into a ProtoRPC object.
        """
        return WatsonQuestionPut(question=self.question,
                                 answer=self.answer)

    @classmethod
    def get_recent_questions(cls, message):
        """
        Builds a message consisting of all the recent questions to Watson
        Returns:
            An instance of WatsonQuestionsListResponse
        """
        q = cls.all()
        q.order('-time_asked')

        questions = [ question.to_message() for question in q.run(limit=message.num_questions) ]

        return WatsonQuestionsListResponse(questions=questions)

    @classmethod
    def put_from_message(cls, message):
        """
        Inserts a new question

        Args:
            message: A WatsonQuestionPut instance to be inserted
        Returns:
            The WatsonQuestion entity that was inserted.
        """
        new_question = cls(question=message.question,
                           answer=message.answer)
        new_question.put()
        return new_question

class GcmCreds(db.Model):
    email = db.StringProperty(required=True)
    reg_id = db.StringProperty(required=True)

    @classmethod
    def put_from_message(cls, message):
        """
        Put's a new device token associated with a user into the DB

        Args:
            message: A GcmCredsPut instance to be inserted
        Returns:
            Nothing
            
        """
        new_creds = cls(email=message.email,
                        reg_id=message.new_reg_id)
        new_creds.put()
        return

    @classmethod
    def get_reg_ids(cls, email):
        all_devices = cls.all()
        all_devices.filter('email =', email)
        reg_ids = []
        for device in all_devices:
            reg_ids.append(device.reg_id)
        return reg_ids

class ClassWeights(db.Model):
    time_taken = db.DateTimeProperty(required=True)
    w1 = db.FloatProperty(required=True)
    w2 = db.FloatProperty(required=True)
    w3 = db.FloatProperty(required=True)
    w4 = db.FloatProperty(required=True)
    w5 = db.FloatProperty(required=True)
    w6 = db.FloatProperty(required=True)
    w7 = db.FloatProperty(required=True)
    w8 = db.FloatProperty(required=True)
    w9 = db.FloatProperty(required=True)
    w10 = db.FloatProperty(required=True)

    @classmethod
    def get_recent_weights(cls):
        """
        Gets most recently stored weights

        Returns:
            A vector of most recent weights
        """
        w = cls.all()
        w.order('-time_taken')
        weights = w.get()
        w_vector = matrix([
            [weights.w1],
            [weights.w2],
            [weights.w3],
            [weights.w4],
            [weights.w5],
            [weights.w6],
            [weights.w7],
            [weights.w8],
            [weights.w9],
            [weights.w10]
        ])
        return w_vector
