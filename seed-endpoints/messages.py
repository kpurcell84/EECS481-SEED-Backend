""" ProtoRPC message class definitions for Seed API """

from protorpc.messages import *
from protorpc.message_types import *


### Doctor Stuff ###

class DoctorPut(Message):
    """ ProtoRPC message definition to represent a doctor """
    first_name = StringField(1, required=True)
    last_name = StringField(2, required=True)
    email = StringField(3, required=True)
    phone = StringField(4, required=True)
    hospital = StringField(5)

### Patient Stuff ###

class PatientPut(Message):
    """ ProtoRPC message definition to represent a patient """
    first_name = StringField(1, required=True)
    last_name = StringField(2, required=True)
    email = StringField(3, required=True)
    phone = StringField(4, required=True)
    doctor_email = StringField(5, required=True)
    diagnosis = StringField(6)
    septic_risk = IntegerField(7)
    basis_pass = StringField(8, required=True)

class PatientListResponse(Message):
    """ ProtoRPC message definition to represent a list of patients reponse """
    patients = MessageField(PatientPut, 1, repeated=True)

class PatientDiagnosisPut(Message):
    """ ProtoRPC message definition to represent a change of a patients diagnosis """
    email = StringField(1, required=True)
    diagnosis = StringField(2, required=True)

### PQuantData Stuff ###

class PQuantDataRequest(Message):
    """ ProtoRPC message definition to represent a patient data query """
    email = StringField(1, required=True)
    start_time = DateTimeField(2, required=True)
    end_time = DateTimeField(3, required=True)

class PQuantDataResponse(Message):
    """ ProtoRPC message definition to represent a single piece of patient data """
    time_taken = DateTimeField(1, required=True)
    blood_pressure = StringField(2)
    body_temp = FloatField(3)
    gsr = FloatField(4)
    skin_temp = FloatField(5)
    air_temp = FloatField(6)
    heart_rate = IntegerField(7)
    activity_type = StringField(8)

class PQuantDataListResponse(Message):
    """ ProtoRPC message definition to represent a set of patient quantitative data (over a period of time) """
    pdata_list = MessageField(PQuantDataResponse, 1, repeated=True)

### PQual Data Stuff ###

class PManDataPut(Message):
    """ ProtoRPC message definition to represent a set of survey responses """
    email = StringField(1, required=True)
    time_taken = DateTimeField(2)
    blood_pressure = StringField(3)
    body_temp = FloatField(4)
    a1 = StringField(5, required=True)
    a2 = StringField(6, required=True)
    a3 = StringField(7, required=True)
    a4 = StringField(8, required=True)
    a5 = StringField(9, required=True)
    a6 = StringField(10, required=True)
    a7 = StringField(11, required=True)
    a8 = StringField(12, required=True)
    a9 = StringField(13, required=True)
    a10 = StringField(14, required=True)

class PQualDataRequest(Message):
    """ ProtoRPC message definition to represent a patient qualitative data query """
    email = StringField(1, required=True)
    start_time = DateTimeField(2, required=True)
    end_time = DateTimeField(3, required=True)

class PQualDataListResponse(Message):
    """ ProtoRPC message definition to represent a set of patient qualitative data (over a period of time) """
    pdata_list = MessageField(PManDataPut, 1, repeated=True)

### Alert Stuff ###

class AlertsRequest(Message):
    email = StringField(1, required=True)
    start_time = DateTimeField(2, required=True)
    end_time = DateTimeField(3, required=True)

class AlertResponse(Message):
    """ ProtoRPC message definition to represent a previously triggered alert """
    patient_email = StringField(1, required=True)
    time_alerted = DateTimeField(2, required=True)
    message = StringField(3, required=True)
    priority = StringField(4, required=True)

class AlertListResponse(Message):
    alerts = MessageField(AlertResponse, 1, repeated=True)

### Watson Stuff ###

class WatsonQuestionPut(Message):
    """ ProtoRPC message definition to represent a watson question/answer pair """
    question = StringField(1, required=True)
    answer = StringField(2, required=True)

class WatsonQuestionsRequest(Message):
    """ ProtoRPC message definition to represent a request for recent watson question/answer pairs """
    num_questions = IntegerField(1, required=True)

class WatsonQuestionsListResponse(Message):
    """ ProtoRPC message definition to represent a list of watson question/answer pair """
    questions = MessageField(WatsonQuestionPut, 1, repeated=True)

### GCM Stuff ###

class GcmCredsPut(Message):
    """ ProtoRPC message definition to represent a user email and Google Cloud Messenger token associated with their device """
    email = StringField(1, required=True)
    new_reg_id = StringField(2)
    old_reg_id = StringField(3)

### General Stuff ###

class EmailRequest(Message):
    """ ProtoRPC message definition to represent an email """
    email = StringField(1, required=True)

class UserCheckResponse(Message):
    """ ProtoRPC message definition to represent a response about the type of user type = (Patient | Doctor | None) """
    user_type = StringField(1, required=True)