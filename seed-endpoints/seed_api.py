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

    @endpoints.method(PatientRequest, PatientResponse,
                      path='patient', http_method='GET',
                      name='patient.get')
    def patient_get(self, request):
        """
        Exposes an API endpoint to query a patient based on patient id

        Args:
            request: An instance of PatientRequest parsed from the API
                request.
        Returns:
            An instance of PatientResponse containing first name and last name
        """
        q = Patient.all()
        q.filter("pid =", PatientRequest.pid)
        result = q.get()
        if result == None:
            print "YOLOOO"
        print result
        return PatientResponse(first_name=result.first_name, last_name=result.last_name)

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


APPLICATION = endpoints.api_server([SeedApi],
                                   restricted=False)