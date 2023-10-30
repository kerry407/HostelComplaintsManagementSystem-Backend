from ..utils.setup import APITestSetup 
from django.urls import reverse 
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from authentication.models import StudentUser, PorterUser
from authentication.api.serializers import StudentSerializer, PorterSerializer

User = get_user_model() 


class HostelAPITestCase(APITestSetup):
    
    def setUp(self) -> None:
        super().setUp()
        refresh = RefreshToken.for_user(self.create_test_superuser())
        access_token = refresh.access_token 
        self.client.credentials(HTTP_AUTHORIZATION= f"Bearer {access_token}")
        
    def test_create_hostel(self):
        data = {
            'name': 'Queen Amina Hall',
            'no_of_rooms': 200,
            'gender': 'female'
        }
        res = self.client.post(path=reverse('hostels-list'), data=data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        
    def test_create_hostel_with_non_enum_choice(self):
        data = {
            'name': 'King James Hall',
            'no_of_rooms': 200,
            'gender': 'male'
        }
        res = self.client.post(path=reverse('hostels-list'), data=data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_hostel_with_non_staff(self):
        refresh = RefreshToken.for_user(self.create_test_student_user())
        access_token = refresh.access_token 
        self.client.credentials(HTTP_AUTHORIZATION= f"Bearer {access_token}")
        
        data = {
            'name': 'Queen Amina Hall',
            'no_of_rooms': 200,
            'gender': 'male'
        }
        res = self.client.post(path=reverse('hostels-list'), data=data)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_list_hostels(self):
        res = self.client.get(path=reverse('hostels-list'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
    def test_retrieve_hostel(self):
        res = self.client.get(path=reverse('hostels-detail', args=[self.hostel.id]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
    def test_partial_update_hostel(self):
        data = {
            'no_of_rooms': 204
        }
        res = self.client.patch(reverse('hostels-detail', args=[self.hostel.id]), data=data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
    def test_delete_hostel(self):
        res = self.client.delete(path=reverse('hostels-detail', args=[self.hostel.id]))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        

        
        