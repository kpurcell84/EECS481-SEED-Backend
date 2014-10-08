from protorpc import remote
from protorpc import messages
from protorpc import message_types

from models import *
from seed_api_messages import *

CLIENT_ID = '264671521534-evjhe6al5t2ahsba3eq2tf8jj78olpei.apps.googleusercontent.com'

@endpoints.api(name='seed', version='v0.1',
               description='A test for passing data through the API',
               allowed_client_ids=[CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID])
class SeedApi(remote.Service):
    """ Class which defines Seed API """

    ### Doctor Stuff ###

    @endpoints.method(DoctorPutMessage, DoctorPutMessage,
                      path='doctor', http_method='POST',
                      name='doctor.put')
    def doctor_insert(self, request):
        """
        Exposes an API endpoint to insert a doctor

        Args:
            request: An instance of DoctorPutMessage parsed from the API
                request.
        Returns:
            An instance of the newly inserted doctor (as a DoctorPutMessage)
        """
        entity = Doctor.put_from_message(request)
        return entity.to_message()

    @endpoints.method(DoctorRequest, DoctorPutMessage,
                      path='doctor', http_method='GET',
                      name='doctor.get')
    def doctor_get(self, request):
        """
        Exposes an API endpoint to query a doctor based on key (email)

        Args:
            request: An instance of DoctorRequest parsed from the API
                request.
        Returns:
            An instance of DoctorPutMessage containing all doctor info
        """
        q = Doctor.all()
        q.filter('__key__ =', Key.from_path('Doctor', request.email))
        doctor = q.get()

        if doctor != None:
            return doctor.to_message() 
        else:
            return DoctorPutMessage(email='None', first_name='None', 
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

    @endpoints.method(PatientPutMessage, PatientPutMessage,
                      path='patient', http_method='POST',
                      name='patient.put')
    def patient_insert(self, request):
        """
        Exposes an API endpoint to insert a patient

        Args:
            request: An instance of PatientPutMessage parsed from the API
                request.
        Returns:
            An instance of the newly inserted patient (as a PatientPutMessage)
        """
        entity = Patient.put_from_message(request)
        return entity.to_message()

    @endpoints.method(PatientRequest, PatientPutMessage,
                  path='patient', http_method='GET',
                  name='patient.get')
    def patient_get(self, request):
        """
        Exposes an API endpoint to query a patient based on key (email)

        Args:
            request: An instance of PatientRequest parsed from the API
                request.
        Returns:
            An instance of PatientPutMessage containing all patient info
        """
        q = Patient.all()
        q.filter('__key__ =', Key.from_path('Patient', request.email))
        patient = q.get()

        if patient != None:
            return patient.to_message() 
        else:
            return PatientPutMessage(email='None', doctor_email='None',
                                    first_name='None', last_name='None', 
                                    phone='None')


APPLICATION = endpoints.api_server([SeedApi],
                                   restricted=False)