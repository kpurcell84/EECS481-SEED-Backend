""" ProtoRPC message class definitions for Seed API """

from protorpc import messages

# Doctor Stuff

class DoctorPutMessage(messages.Message):
	""" ProtoRPC message definition to represent a doctor """
	did = messages.IntegerField(1, required=True)
	first_name = messages.StringField(2, required=True)
	last_name = messages.StringField(3, required=True)
	email = messages.StringField(4, required=True)
	phone = messages.StringField(5, required=True)
	hospital = messages.StringField(6)

# Patient Stuff

class PatientRequest(messages.Message):
	""" ProtoRPC message definition to represent a patient query """
	pid = messages.IntegerField(1)

class PatientResponse(messages.Message):
	""" ProtoRPC message definition to represent a patient response """
	first_name = messages.StringField(1)
	last_name = messages.StringField(2)

class PatientListResponse(messages.Message):
	""" ProtoRPC message definition to represent a list of patients reponse """
	patients = messages.MessageField(PatientRequest, 1, repeated=True)