from tests.utils.setup import APITestSetup
from authentication.models import Hostel, StudentUser, PorterUser


class HostelModelTestCase(APITestSetup):
    
    def test_hostel_model_name(self):
        self.assertEqual(self.hostel.name, 'Professor Biobaku Hall')
