from protorpc import remote
from protorpc import messages
from protorpc import message_types

from datetime import datetime

from models import *
from generate import generate_sample_data
from seed_api_messages import *

CLIENT_ID = '264671521534-evjhe6al5t2ahsba3eq2tf8jj78olpei.apps.googleusercontent.com'

@endpoints.api(name='seed', version='v0.4.4',
               description='A test for passing data through the API',
               allowed_client_ids=[CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID])
class SeedApi(remote.Service):
    """ Class which defines Seed API """

#####################
### General Stuff ###
#####################
    @endpoints.method(message_types.VoidMessage, 
                      message_types.VoidMessage,
                      path='generate', http_method='POST',
                      name='generate.put')
    def generate_data(self, request):
        """
        Exposes an API endpoint to generate a random data set for testing.
        Only run once.
        Data set parameters adjustable in the backend
        """
        generate_sample_data()
        return message_types.VoidMessage()

####################
### Doctor Stuff ###
####################
    @endpoints.method(DoctorPut, message_types.VoidMessage,
                      path='doctor', http_method='POST',
                      name='doctor.put')
    def doctor_put(self, request):
        """
        Exposes an API endpoint to insert a doctor

        Args:
            request: An instance of DoctorPut parsed from the API
                request.
        Returns:
            Nothing
        """
        Doctor.put_from_message(request)
        return message_types.VoidMessage()

    @endpoints.method(DoctorRequest, DoctorPut,
                      path='doctor', http_method='GET',
                      name='doctor.get')
    def doctor_get(self, request):
        """
        Exposes an API endpoint to query a doctor based on key (email)

        Args:
            request: An instance of DoctorRequest parsed from the API
                request.
        Returns:
            An instance of DoctorPut containing all doctor info
        """
        q = Doctor.all()
        q.filter('__key__ =', Key.from_path('Doctor', request.email))
        doctor = q.get()

        if doctor != None:
            return doctor.to_message() 
        else:
            return DoctorPut(email='None', first_name='None', 
                                    last_name='None', phone='None')

    @endpoints.method(DoctorRequest, PatientListResponse,
                      path='doctors_patients', http_method='POST',
                      name='doctors_patients.get')
    def doctors_patients_get(self, request):
        """
        Exposes an API endpoint to query all a doctors patients based on the doctor's key (email)

        Args:
            request: An instance of DoctorRequest parsed from the API
                request.
        Returns:
            An instance of PatientListResponse containing all doctor info
        """
        q = Doctor.all()
        q.filter('__key__ =', Key.from_path('Doctor', request.email))
        doctor = q.get()

        if doctor != None:
            return doctor.get_patients() 
        else:
            return PatientListResponse(patients=[])

    @endpoints.method(DoctorRequest, AlertListResponse,
                      path='doctor_alerts', http_method='POST',
                      name='doctor_alerts.get')
    def doctor_alerts_get(self, request):
        """
        Exposes an API endpoint to get all of a doctors patients alerts

        Args:
            request: An instance of DoctorRequest parsed from the API request.
        Returns:
            An AlertListResponse message
        """
        q = Doctor.all()
        q.filter('__key__ =', Key.from_path('Doctor', request.email))
        doctor = q.get()

        if doctor != None:
            return doctor.get_alerts()
        else:
            return AlertListResponse()

#####################
### Patient Stuff ###
#####################
    @endpoints.method(PatientPut, PatientPut,
                      path='patient', http_method='POST',
                      name='patient.put')
    def patient_put(self, request):
        """
        Exposes an API endpoint to insert a patient

        Args:
            request: An instance of PatientPut parsed from the API
                request.
        Returns:
            An instance of the newly inserted patient (as a PatientPut)
        """
        entity = Patient.put_from_message(request)
        return entity.to_message()

    @endpoints.method(PatientRequest, PatientPut,
                  path='patient', http_method='GET',
                  name='patient.get')
    def patient_get(self, request):
        """
        Exposes an API endpoint to query a patient based on key (email)

        Args:
            request: An instance of PatientRequest parsed from the API
                request.
        Returns:
            An instance of PatientPut containing all patient info
        """
        q = Patient.all()
        q.filter('__key__ =', Key.from_path('Patient', request.email))
        patient = q.get()

        if patient != None:
            return patient.to_message() 
        else:
            return PatientPut(email='None', doctor_email='None',
                                    first_name='None', last_name='None', 
                                    phone='None')

    @endpoints.method(PatientDiagnosisPut, message_types.VoidMessage,
                      path='patient_diagnosis', http_method='POST',
                      name='patient_diagnosis.put')
    def patient_diagnosis_put(self, request):
        """
        Exposes an API endpoint to set a patients diagnosis (to be called by a doctor) 

        Args:
            request: An instance of PatientDiagnosisPut parsed from the API request.
        Returns:
            Nothing
        """
        q = Patient.all()
        q.filter('__key__ =', Key.from_path('Patient', request.email))
        patient = q.get()

        if patient != None:
            patient.diagnosis = request.diagnosis
            patient.put()

        return message_types.VoidMessage()

    @endpoints.method(PatientManualDataPut, message_types.VoidMessage,
                      path='patient_man_data_put', http_method='POST',
                      name='patient_man_data.put')
    def patient_man_data_put(self, request):
        """
        Exposes an API endpoint to insert a patient's manual quantitative data into the datastore

        Args:
            request: An instance of PatientManualDataPut parsed from the API request.
        Returns:
            Nothing
        """
        q = Patient.all()
        q.filter('__key__ =', Key.from_path('Patient', request.email))
        patient = q.get()

        if patient != None:
            time_taken = datetime.now()
            new_datum = PQuantData(patient=patient,
                                   time_taken=time_taken,
                                   blood_pressure=request.blood_pressure,
                                   body_temp=request.body_temp)
            new_datum.put()

        return message_types.VoidMessage()

##################
### Data Stuff ###
##################
    @endpoints.method(PQuantDataRequest, PQuantDataListResponse,
                      path='p_quant_data', http_method='POST',
                      name='p_quant_data.get')
    def p_quant_data_get(self, request):
        """
        Exposes an API endpoint to get quantitative patient data based on a time range

        Args:
            request: An instance of PQuantDataRequest parsed from the API
                request.
        Returns:
            An instance of the PQuantDataListResponse containing the requested patient data within the requested time range (inclusive)
        """
        q = Patient.all()
        q.filter('__key__ =', Key.from_path('Patient', request.email))
        patient = q.get()

        if patient != None:
            return PQuantData.get_range(request, patient)
        else:
            return PQuantDataListResponse()

    @endpoints.method(PQualDataRequest, PQualDataListResponse,
                      path='p_qual_data_get', http_method='POST',
                      name='p_qual_data.get')
    def p_qual_data_get(self, request):
        """
        Exposes an API endpoint to get qualitative patient data based on a time range

        Args:
            request: An instance of PQualDataRequest parsed from the API
                request.
        Returns:
            An instance of the PQualDataListResponse containing the requested patient survey responses within the requested time range (inclusive)
        """
        q = Patient.all()
        q.filter('__key__ =', Key.from_path('Patient', request.email))
        patient = q.get()

        if patient != None:
            return PQualData.get_range(request, patient)
        else:
            return PQualDataListResponse()

    @endpoints.method(PQualDataPut, message_types.VoidMessage,
                      path='p_qual_data_put', http_method='POST',
                      name='p_qual_data.put')
    def p_qual_data_put(self, request):
        """
        Exposes an API endpoint to inserting qualitative patient data from the survey

        Args:
            request: An instance of PQualDataPut parsed from the API
                request.
        Returns:
            Nothing
        """
        q = Patient.all()
        q.filter('__key__ =', Key.from_path('Patient', request.email))
        patient = q.get()

        if patient != None:
            PQualData.put_from_message(request, patient)
            return message_types.VoidMessage()
        else:
            return message_types.VoidMessage()

###################
### Alert Stuff ###
###################
    @endpoints.method(PatientRequest, AlertListResponse,
                      path='alerts', http_method='POST',
                      name='alerts.get')
    def alerts_get(self, request):
        """
        Exposes an API endpoint to get alerts associated with a user

        Args:
            request: An instance of AlertRequest parsed from the API request.
        Returns:
            An AlertListResponse message, for a patients contains all of their emergency alerts, for a doctor contains all of their patient's alerts
        """
        q1 = Patient.all()
        q2 = Doctor.all()
        q1.filter('__key__ =', Key.from_path('Patient', request.email))
        q2.filter('__key__ =', Key.from_path('Doctor', request.email))
        patient = q1.get()
        doctor = q2.get()

        if patient != None:
            return Alert.get_alerts(patient, "Patient")
        elif doctor != None:
            return Alert.get_alerts(doctor, "Doctor")
        else:
            return AlertListResponse()

####################
### Watson Stuff ###
####################
    @endpoints.method(WatsonQuestionPut, message_types.VoidMessage,
                      path='watson_question', http_method='POST',
                      name='watson_question.put')
    def watson_question_put(self, request):
        """
        Exposes an API endpoint to insert a watson question/answer pair

        Args:
            request: An instance of WatsonQuestionPut parsed from the API
                request.
        Returns:
            Nothing
        """
        WatsonQuestion.put_from_message(request)
        return message_types.VoidMessage()

    @endpoints.method(WatsonQuestionsRequest, WatsonQuestionsListResponse,
                      path='watson_recent_questions', http_method='POST',
                      name='watson_recent_questions.get')
    def watson_recent_questions_get(self, request):
        """
        Exposes an API endpoint to query the n most recent questions patients have asked watson

        Args:
            request: An instance of WatsonQuestionsRequest parsed from the API
                request.
        Returns:
            An list of the n most recent questions (as a WatsonQuestionListResponse)
        """
        return WatsonQuestion.get_recent_questions(request)

#################
### GCM Stuff ###
#################
    @endpoints.method(GcmCredsPut, message_types.VoidMessage,
                      path='gcm_creds', http_method='POST',
                      name='gcm_creds.put')
    def gmc_creds_put(self, request):
        """
        Exposes an API endpoint to insert a GCM email/token pair

        Args:
            request: An instance of GcmCredsPut parsed from the API
                request.
        Returns:
            Nothing
        """
        if request.old_reg_id != None:
            q = GcmCreds.all()
            q.filter('reg_id =', request.old_reg_id)
            old_creds = q.get()
            if old_creds != None:
                old_creds.delete()

        GcmCreds.put_from_message(request)
        return message_types.VoidMessage()

#####################
### General Stuff ###
#####################
    @endpoints.method(UserCheckRequest, UserCheckResponse,
                      path='user_check', http_method='POST',
                      name='user_check.get')
    def user_check_get(self, request):
        """
        Exposes an API endpoint to check the type of user

        Args:
            request: An instance of UserCheckRequest parsed from the API request.
        Returns:
            A UserCheckResponse object indicating what type of user the email is (Doctor | Patient | None)
        """
        q1 = Patient.all()
        q2 = Doctor.all()
        q1.filter('__key__ =', Key.from_path('Patient', request.email))
        q2.filter('__key__ =', Key.from_path('Doctor', request.email))
        patient = q1.get()
        doctor = q2.get()

        if patient != None:
            return UserCheckResponse(user_type='Patient')
        elif doctor != None:
            return UserCheckResponse(user_type='Doctor')
        else:
            return UserCheckResponse(user_type='None')


APPLICATION = endpoints.api_server([SeedApi],
                                   restricted=False)