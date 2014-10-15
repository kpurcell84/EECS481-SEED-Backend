""" ProtoRPC message class definitions for Seed API """

from protorpc import messages, message_types

### Doctor Stuff ###

class DoctorPutMessage(messages.Message):
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

class PatientPutMessage(messages.Message):
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
    patients = messages.MessageField(PatientPutMessage, 1, repeated=True)

### PData Stuff ###

class PDataRandomPut(messages.Message):
    """ ProtoRPC message definition to represent info for generating random patient data for testing
        - email is patient email
        - frequency is in minutes 
    """
    email = messages.StringField(1, required=True)
    start_time = message_types.DateTimeField(2, required=True)
    end_time = message_types.DateTimeField(3, required=True)
    frequency = messages.IntegerField(4, required=True)

class PDataRequest(messages.Message):
    """ ProtoRPC message definition to represent a patient data query """
    email = messages.StringField(1, required=True)
    start_time = message_types.DateTimeField(2, required=True)
    end_time = message_types.DateTimeField(3, required=True)

class PDataResponse(messages.Message):
    """ ProtoRPC message definition to represent a single piece of patient data """
    time_taken = message_types.DateTimeField(1, required=True)
    blood_pressure = messages.StringField(2)
    body_temp = messages.FloatField(3)
    heart_rate = messages.IntegerField(4)

class PDataListResponse(messages.Message):
    """ ProtoRPC message definition to represent a set of patient data (over a period of time) """
    pdata_list = messages.MessageField(PDataResponse, 1, repeated=True)

### Watson Stuff ###

class WatsonQuestionPutMessage(messages.Message):
    """ ProtoRPC message definition to represent a watson question/answer pair """
    question = messages.StringField(1, required=True)
    answer = messages.StringField(2, required=True)

class WatsonQuestionsRequest(messages.Message):
    """ ProtoRPC message definition to represent a request for recent watson question/answer pairs """
    num_questions = messages.IntegerField(1, required=True)

class WatsonQuestionsListResponse(messages.Message):
    """ ProtoRPC message definition to represent a list of watson question/answer pair """
    questions = messages.MessageField(WatsonQuestionPutMessage, 1, repeated=True)


