from authentication.models import *
from tests.utils.setup import APITestSetup


class CustomUserModelTestCase(APITestSetup):
    
    def test_custom_student_user_creation(self):
        user = self.create_test_student_user()
        self.assertEqual(user.matric_number, '180401004')
        self.assertTrue(user.is_student)
        
    def test_custom_porter_user_creation(self):
        user = self.create_test_porter_user()
        self.assertEqual(user.matric_number, None)
        self.assertTrue(user.is_porter)
        
        
        


        
        
    
        
     
        
