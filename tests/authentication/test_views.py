from ..utils.setup import APITestSetup 
from django.urls import reverse 
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from authentication.models import StudentUser, PorterUser

User = get_user_model()
class AuthTestCase(APITestSetup):
    
    def setUp(self) -> None:
        super().setUp()
        self.student_user = self.create_test_student_user()
        self.porter = self.create_test_porter_user()
        
    
    def test_student_user_sign_up(self):
        url = reverse("create-student-account")
        user_data = {
        "first_name": "Preston",
        "last_name": "Nwokocha",
        "matric_number": "190802003",
        "email": "preston@example.com",
        "hostel": self.hostel.id,
        "gender": "male",
        "password": "Akpororo1",
        "password2": "Akpororo1"
        }
        res = self.client.post(url, user_data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(matric_number="190802003")
        self.assertTrue(user.is_student)
        self.assertFalse(user.is_porter)
        self.assertTrue(StudentUser.objects.filter(user=user).exists())
        
    def test_porter_user_sign_up(self):
        url = reverse("create-porter-account")
        user_data = {
        "first_name": "Mike",
        "last_name": "Nwokocha",
        "email": "mike@example.com",
        "hostel": self.hostel.id,
        "gender": "male",
        "password": "Akpororo1",
        "password2": "Akpororo1"
        }
        res = self.client.post(url, user_data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email="mike@example.com")
        self.assertTrue(user.is_porter)
        self.assertFalse(user.is_student)
        self.assertTrue(PorterUser.objects.filter(user=user).exists())
        
        
    def test_login_student_user(self):
        login_data = {
            "matric_number": "180401004",
            "password": "testpassword1"
        }
        res = self.client.post(reverse("student-login"), login_data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
    def test_login_porter_user(self):
        login_data = {
            "email": "test2@test.com",
            "password": "testpassword1"
        }
        res = self.client.post(reverse("porter-login"), login_data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
    def test_login_student_user_with_invalid_credentials(self):
        login_data = {
            "matric_number": "180401004",
            "password": "Akpororo1"
        }
        res = self.client.post(reverse("student-login"), login_data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_login_porter_user_with_invalid_credentials(self):
        login_data = {
            "email": "test2@test.com",
            "password": "Akpororo1"
        }
        res = self.client.post(reverse("porter-login"), login_data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_refresh_token(self):
        url = reverse('login-refresh')
        data = {
            "refresh": str(RefreshToken.for_user(self.student_user))
        }
        res = self.client.post(url, data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
      
    def test_users_list(self):
        refresh = RefreshToken.for_user(self.create_test_superuser())
        access_token = refresh.access_token 
        self.client.credentials(HTTP_AUTHORIZATION= f"Bearer {access_token}")
        res = self.client.get(path=reverse('users-list'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.wsgi_request.user.is_staff)
        
    def test_users_list_with_non_staff(self):
        refresh = RefreshToken.for_user(self.student_user)
        access_token = refresh.access_token 
        self.client.credentials(HTTP_AUTHORIZATION= f"Bearer {access_token}")
        res = self.client.get(path=reverse('users-list'))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(res.wsgi_request.user.is_staff)