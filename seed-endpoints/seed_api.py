from protorpc import remote
from protorpc import messages
from protorpc import message_types

from models import *
from generate import *
from seed_api_messages import *

CLIENT_ID = '264671521534-evjhe6al5t2ahsba3eq2tf8jj78olpei.apps.googleusercontent.com'

@endpoints.api(name='seed', version='v0.3',
               description='A test for passing data through the API',
               allowed_client_ids=[CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID])
class SeedApi(remote.Service):
    """ Class which defines Seed API """

    ### General Stuff ###

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

    ### Doctor Stuff ###

    @endpoints.method(DoctorPut, DoctorPut,
                      path='doctor', http_method='POST',
                      name='doctor.put')
    def doctor_put(self, request):
        """
        Exposes an API endpoint to insert a doctor

        Args:
            request: An instance of DoctorPut parsed from the API
                request.
        Returns:
            An instance of the newly inserted doctor (as a DoctorPut)
        """
        entity = Doctor.put_from_message(request)
        return entity.to_message()

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
    
    ### Patient Stuff ###

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

    ### Data Stuff ###

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
            return PQuantData.get_range(request)
        else:
            return PQuantDataResponse()

    @endpoints.method(PQualDataPut, message_types.VoidMessage,
                      path='p_qual_data', http_method='POST',
                      name='p_qual_data.put')
    def p_qual_data_put(self, request):
        """
        Exposes an API endpoint to inserting qualitative patient data from the survey

        Args:
            request: An instance of PQuantDataPut parsed from the API
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

    ### Watson Stuff ###

    @endpoints.method(WatsonQuestionPut, WatsonQuestionPut,
                      path='watson_question', http_method='POST',
                      name='watson_question.put')
    def watson_question_put(self, request):
        """
        Exposes an API endpoint to insert a watson question/answer pair

        Args:
            request: An instance of WatsonQuestionPut parsed from the API
                request.
        Returns:
            An instance of the newly inserted question (as a WatsonQuestionPut)
        """
        entity = WatsonQuestion.put_from_message(request)
        return entity.to_message()

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




APPLICATION = endpoints.api_server([SeedApi],
                                   restricted=False)