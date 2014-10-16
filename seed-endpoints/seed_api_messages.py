""" ProtoRPC message class definitions for Seed API """

from protorpc import messages, message_types

### Doctor Stuff ###

class DoctorPut(messages.Message):
    """ ProtoRPC message definition to represent a doctor """
    first_name = messages.StringField(1, required=True)
    last_name = messages.StringField(2, required=True)
    email = messages.StringField(3, required=True)
    phone = messages.StringField(4, required=True)
    hospital = messages.StringField(5)

class DoctorRequest(messages.Message):
    """ ProtoRPC message definition to represent a doctor query """
    email = messages.StringField(1)

### Patient Stuff ###

class PatientPut(messages.Message):
    """ ProtoRPC message definition to represent a patient """
    first_name = messages.StringField(1, required=True)
    last_name = messages.StringField(2, required=True)
    email = messages.StringField(3, required=True)
    phone = messages.StringField(4, required=True)
    doctor_email = messages.StringField(5, required=True)

class PatientRequest(messages.Message):
    """ ProtoRPC message definition to represent a patient query """
    email = messages.StringField(1)

class PatientListResponse(messages.Message):
    """ ProtoRPC message definition to represent a list of patients reponse """
    patients = messages.MessageField(PatientPut, 1, repeated=True)

### PQuantData Stuff ###

class PQuantDataRandomPut(messages.Message):
    """ ProtoRPC message definition to represent info for generating random patient data for testing
        - email is patient email
        - frequency is in minutes 
    """
    email = messages.StringField(1, required=True)
    start_time = message_types.DateTimeField(2, required=True)
    end_time = message_types.DateTimeField(3, required=True)
    frequency = messages.IntegerField(4, required=True)

class PQuantDataRequest(messages.Message):
    """ ProtoRPC message definition to represent a patient data query """
    email = messages.StringField(1, required=True)
    start_time = message_types.DateTimeField(2, required=True)
    end_time = message_types.DateTimeField(3, required=True)

class PQuantDataResponse(messages.Message):
    """ ProtoRPC message definition to represent a single piece of patient data """
    time_taken = message_types.DateTimeField(1, required=True)
    blood_pressure = messages.StringField(2)
    body_temp = messages.FloatField(3)
    gsr = messages.FloatField(4)
    skin_temp = messages.FloatField(5)
    air_temp = messages.FloatField(6)
    heart_rate = messages.IntegerField(7)
    activity_type = messages.StringField(8)
    toss_or_turn = messages.StringField(9)

class PQuantDataListResponse(messages.Message):
    """ ProtoRPC message definition to represent a set of patient data (over a period of time) """
    pdata_list = messages.MessageField(PQuantDataResponse, 1, repeated=True)

### PQual Data Stuff ###


### Watson Stuff ###

class WatsonQuestionPut(messages.Message):
    """ ProtoRPC message definition to represent a watson question/answer pair """
    question = messages.StringField(1, required=True)
    answer = messages.StringField(2, required=True)

class WatsonQuestionsRequest(messages.Message):
    """ ProtoRPC message definition to represent a request for recent watson question/answer pairs """
    num_questions = messages.IntegerField(1, required=True)

class WatsonQuestionsListResponse(messages.Message):
    """ ProtoRPC message definition to represent a list of watson question/answer pair """
    questions = messages.MessageField(WatsonQuestionPut, 1, repeated=True)


