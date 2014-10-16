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

class DoctorRequest(Message):
    """ ProtoRPC message definition to represent a doctor query """
    email = StringField(1)

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

class PatientRequest(Message):
    """ ProtoRPC message definition to represent a patient query """
    email = StringField(1)

class PatientListResponse(Message):
    """ ProtoRPC message definition to represent a list of patients reponse """
    patients = MessageField(PatientPut, 1, repeated=True)

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
    toss_or_turn = StringField(9)

class PQuantDataListResponse(Message):
    """ ProtoRPC message definition to represent a set of patient data (over a period of time) """
    pdata_list = MessageField(PQuantDataResponse, 1, repeated=True)

### PQual Data Stuff ###

class PQualDataPut(Message):
    """ ProtoRPC message definition to represent a set of survey responses """
    email = StringField(1, required=True)
    time_taken = DateTimeField(2, required=True)
    a1 = IntegerField(3, required=True)

### Alert Stuff ###

class AlertResponse(Message):
    """ ProtoRPC message definition to represent a previously triggered alert """
    time_alerted = DateTimeField(1, required=True)
    message = StringField(2, required=True)
    priority = StringField(3, required=True)

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


