from django.test import TestCase  
from django.contrib.auth import get_user_model 
from authentication.models import CustomUser
from rest_framework.test import APITestCase
from typing import Dict, Any 
from authentication.api.serializers import * 
from dashboard.api.serializers import HostelSerializer
User = get_user_model()


class APITestSetup(APITestCase):
    
    def setUp(self) -> None:
        print(f"Starting test for {str(self)}...")
        
        hostel_serializer = HostelSerializer(data={
            'name': 'Professor Biobaku Hall',
            'no_of_rooms': 200,
            'gender': 'male'
        })
        hostel_serializer2 = HostelSerializer(data={
            'name': 'King Jaja Hall',
            'no_of_rooms': 205,
            'gender': 'male'
        })
        hostel_serializer.is_valid(raise_exception=True)
        hostel_serializer2.is_valid(raise_exception=True)
        self.hostel = hostel_serializer.save()
        self.hostel2 = hostel_serializer2.save()
        print("---------------")
        return super().setUp()
        
    def create_test_student_user(self, **kwargs: Dict[str, Any]) -> CustomUser:
        user_serializer = AccountSerializer(data={
            'email': 'test@test.com',
            'matric_number': '180401004',
            'first_name': 'test',
            'gender': 'male',
            'hostel': self.hostel.id,
            'last_name': 'test&test',
            'password': 'testpassword1',
            'password2': 'testpassword1'
        })
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save(is_student=True)
        return user
    
    def create_test_porter_user(self, **kwargs: Dict[str, Any]) -> CustomUser:
        user_serializer = PorterAccountSerializer(data={
            'email': 'test2@test.com',
            'first_name': 'test',
            'gender': 'male',
            'hostel': self.hostel.id,
            'last_name': 'test&test',
            'password': 'testpassword1',
            'password2': 'testpassword1'
        })
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save(is_porter=True)
        return user
    
    def create_test_superuser(self) -> CustomUser:
        user = User.objects.create_superuser(
                                            email="kerry@admin.com", 
                                            password="Akpororo1",
                                            hostel=self.hostel
                                            ) 
        return user 
    
    def tearDown(self) -> None:
        print(f"Finished test for {str(self)}...")
        print("---------------")
        return super().tearDown()
    
     
        
