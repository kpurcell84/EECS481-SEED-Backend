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
        Turns the Doctor entity into a ProtoRPC object. This is necessary so the entity can be returned in an API request.
        Returns:
            An instance of DoctorPutMessage
        """
        return DoctorPutMessage(email=self.key().name(),
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
            message: A DoctorPutMessage instance to be inserted, note that the email is used as the entity key
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
    doctor = db.ReferenceProperty(Doctor)
    first_name = db.StringProperty(required=True)
    last_name = db.StringProperty(required=True)
    phone = db.PhoneNumberProperty(required=True)

    def to_message(self):
        """
        Turns the Patient entity into a ProtoRPC object. This is necessary so the entity can be returned in an API request.
        Returns:
            An instance of PatientPutMessage
        """
        return PatientPutMessage(email=self.key().name(),
                                first_name=self.first_name,
                                last_name=self.last_name,
                                phone=self.phone,
                                doctor_email=self.doctor.key().name())

    @classmethod
    def put_from_message(cls, message):
        """
        Inserts a patient into the DB

        Args:
            message: A PatientPutMessage instance to be inserted.
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
                        phone=message.phone)
        new_patient.put()
        return new_patient


class PData(db.Model):
    patient = db.ReferenceProperty(Patient)
    date_taken = db.DateTimeProperty()
    blood_pressure = db.StringProperty()
    body_temp = db.IntegerProperty()
    heart_rate = db.IntegerProperty()
