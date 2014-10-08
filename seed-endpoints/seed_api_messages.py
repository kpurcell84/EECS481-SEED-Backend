""" ProtoRPC message class definitions for Seed API """

from protorpc import messages

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