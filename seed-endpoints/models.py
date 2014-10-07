"""
Defines the models for the backend datastore
"""

from google.appengine.ext import endpoints
from google.appengine.ext import db

from seed_api_messages import *

class Doctor(db.Model):
    did = db.IntegerProperty()
    first_name = db.StringProperty(required=True)
    last_name = db.StringProperty(required=True)
    email = db.EmailProperty(required=True)
    phone = db.PhoneNumberProperty(required=True)
    hospital = db.StringProperty()

    def to_message(self):
        """
        Turns the Doctor entity into a ProtoRPC object. This is necessary so the entity can be returned in an API request.
        Returns:
            An instance of DoctorPutMessage
        """
        return DoctorPutMessage(did=self.did,
                        first_name=self.first_name,
                        last_name=self.last_name,
                        email=self.email,
                        phone=self.phone,
                        hospital=self.hospital)

    @classmethod
    def put_from_message(cls, message):
        """
        Inserts a doctor into the DB

        Args:
            message: A DoctorPutMessage instance to be inserted.
        Returns:
            The Doctor entity that was inserted.
        """
        new_doctor = cls(did=message.did,
                        first_name=message.first_name,
                        last_name=message.last_name,
                        email=message.email,
                        phone=message.phone,
                        hospital=message.hospital)
        new_doctor.put()
        return new_doctor


class Patient(db.Model):
    pid = db.IntegerProperty()
    doctor = db.ReferenceProperty(Doctor)
    first_name = db.StringProperty(required=True)
    last_name = db.StringProperty(required=True)
    email = db.EmailProperty(required=True)
    phone = db.PhoneNumberProperty(required=True)


class PatientData(db.Model):
    patient = db.ReferenceProperty(Patient)
    date_taken = db.DateTimeProperty()
    blood_pressure = db.StringProperty()
    body_temp = db.IntegerProperty()
    heart_rate = db.IntegerProperty()
