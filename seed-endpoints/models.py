"""
Defines the models for the backend datastore
"""

from google.appengine.ext import endpoints
from google.appengine.ext import db

from google.appengine.api.datastore import Key

from seed_api_messages import *

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
    septic_risk = db.IntegerProperty(required=True)

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
                            septic_risk=self.septic_risk)

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
                        septic_risk=-1)
        new_patient.put()
        return new_patient


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
    toss_or_turn = db.StringProperty() # Yes|No

    def to_message(self):
        """
        Turns the PData entity into a ProtoRPC object.
        """
        return PQuantDataResponse(time_taken=self.time_taken,
                            blood_pressure=self.blood_pressure,
                            body_temp=self.body_temp,
                            gsr = self.gsr,
                            skin_temp = self.skin_temp,
                            air_temp = self.air_temp,
                            heart_rate = self.heart_rate,
                            activity_type = self.activity_type,
                            toss_or_turn = self.toss_or_turn)

    @classmethod
    def get_range(cls, message):
        """
        Builds a message consisting of all the available patient data within the requested time range
        Returns:
            An instance of PDataListResponse
        """
        q = Patient.all()
        q.filter('__key__ =', Key.from_path('Patient', message.email))
        patient = q.get()

        q = cls.all()
        q.filter('patient =', patient)
        q.filter('time_taken >=', message.start_time)
        q.filter('time_taken <=', message.end_time)
        q.order('time_taken')

        pdata_list = [ pdata.to_message() for pdata in q.run() ]

        return PDataListResponse(pdata_list=pdata_list)

class PQualData(db.Model):
    patient = db.ReferenceProperty(Patient, required=True)
    time_taken = db.DateTimeProperty(required=True)
    a1 = db.IntegerProperty(required=True) # 1-5
    # TODO add more answers

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
                        a1=message.a1)
        new_datum.put()
        return

class Alert(db.Model):
    patient = db.ReferenceProperty(Patient, required=True)
    time_alerted = db.DateTimeProperty(required=True)
    message = db.StringProperty(required=True)
    priority = db.StringProperty(required=True) # Early|Emergency

    def to_message(self):
        """
        Turns the Alert entity into a ProtoRPC object. 
        """
        return AlertResponse(time_alerted=self.time_alerted,
                             message=self.message,
                             priority=self.priority)

class WatsonQuestion(db.Model):
    question = db.StringProperty(required=True)
    answer = db.StringProperty(required=True)
    date_asked = db.DateTimeProperty(auto_now_add=True)

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
        q.order('-date_asked')

        questions = [ question.to_message() for question in q.run(limit=message.num_questions) ]

        return WatsonQuestionsListResponse(questions=questions)

    @classmethod
    def put_from_message(cls, message):
        """
        Inserts a doctor into the DB

        Args:
            message: A DoctorPut instance to be inserted, note that the email is used as the entity key
        Returns:
            The Doctor entity that was inserted.
        """
        new_question = cls(question=message.question,
                           answer=message.answer)
        new_question.put()
        return new_question