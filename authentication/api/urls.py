from django.urls import path 
from . import views 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path("sign-up/", views.AccountCreateView.as_view(), name="create-account"),
    path("students/login/", views.StudentTokenObtainPairViewSet.as_view(), name='student_token_obtain_pair'),
    path("porters/login/", views.PorterTokenObtainPairViewSet.as_view(), name='porter_token_obtain_pair'),
    path("login/refresh/", TokenRefreshView.as_view(), name='token_refresh'),   
]


