from ..utils.setup import APITestSetup 
from django.urls import reverse 
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from authentication.models import StudentUser, PorterUser, CustomUser
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
        
        
class StudentAPITestCase(APITestSetup):
    
    def setUp(self) -> None:
        super().setUp()
        self.student_user = self.create_test_student_user()
        refresh = RefreshToken.for_user(self.student_user)
        access_token = refresh.access_token 
        self.client.credentials(HTTP_AUTHORIZATION= f"Bearer {access_token}")
    
    def test_list_students(self):
        res = self.client.get(path=reverse('students-list'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
    def test_retrieve_student(self):
        res = self.client.get(path=reverse('students-detail', args=[self.student_user.id]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
    def test_update_student(self):
        data = {
            'faculty': 'Engineering',
            'department': 'Chemical Engineering',
            'room_no': '120',
            'block_no': 'A12'
        }
        res = self.client.put(path=reverse('students-detail', args=[self.student_user.id]), data=data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
    def test_partial_update_student(self):
        data = {
            'room_no': '143',
            'block_no': 'B14'
        }
        res = self.client.put(path=reverse('students-detail', args=[self.student_user.id]), data=data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
    def test_update_student_with_non_creator(self):
        user = CustomUser.objects.create(email='testcreateuser@test.com', hostel=self.hostel)
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token 
        self.client.credentials(HTTP_AUTHORIZATION= f"Bearer {access_token}")
        data = {
            'faculty': 'Engineering',
            'department': 'Chemical Engineering',
            'room_no': '120',
            'block_no': 'A12'
        }
        res = self.client.put(path=reverse('students-detail', args=[self.student_user.id]), data=data)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        
        
    def test_partial_update_student_with_non_creator(self):
        user = CustomUser.objects.create(email='testcreateuser@test.com', hostel=self.hostel)
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token 
        self.client.credentials(HTTP_AUTHORIZATION= f"Bearer {access_token}")
        data = {
            'room_no': '143',
            'block_no': 'B14'
        }
        res = self.client.put(path=reverse('students-detail', args=[self.student_user.id]), data=data)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_delete_student(self):
        res = self.client.delete(path=reverse('students-detail', args=[self.student_user.id]))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
    
        
class PorterAPITestCase(APITestSetup):
    
    def setUp(self) -> None:
        super().setUp()
        self.porter_user = self.create_test_porter_user()
        refresh = RefreshToken.for_user(self.porter_user)
        access_token = refresh.access_token 
        self.client.credentials(HTTP_AUTHORIZATION= f"Bearer {access_token}")
    
    def test_list_porters(self):
        res = self.client.get(path=reverse('porters-list'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
    def test_retrieve_porter(self):
        res = self.client.get(path=reverse('porters-detail', args=[self.porter_user.id]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
    def test_delete_portert(self):
        res = self.client.delete(path=reverse('porters-detail', args=[self.porter_user.id]))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
    

class DashBoardAPITestCase(APITestSetup):
    
    def setUp(self) -> None:
        super().setUp()
        self.porter_user = self.create_test_porter_user()
        self.student_user = self.create_test_student_user()
        refresh = RefreshToken.for_user(self.porter_user)
        access_token = refresh.access_token 
        self.client.credentials(HTTP_AUTHORIZATION= f"Bearer {access_token}")
        
    def test_dashboard_count_view(self):
        res = self.client.get(path=reverse('dashboard-count'))
        results = res.json()['data']
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(results['student_count'], 1)
        self.assertEqual(results['porter_count'], 1)
        self.assertEqual(results['hostel_gender'], res.wsgi_request.user.gender)
        
