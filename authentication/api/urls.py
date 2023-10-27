from django.urls import path 
from . import views 
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path("student-sign-up/", views.StudentAccountCreateView.as_view(), name="create-student-account"),
    path("porter-sign-up/", views.PorterAccountCreateView.as_view(), name="create-porter-account"),
    path("user-details/<str:pk>/", views.AccountDetailsView.as_view(), name="user-details"),
    path("users-list/", views.AccountsListView.as_view(), name="users-list"),
    path("students/login/", views.StudentTokenObtainPairViewSet.as_view(), name='student-login'),
    path("porters/login/", views.PorterTokenObtainPairViewSet.as_view(), name='porter-login'),
    path("login/refresh/", TokenRefreshView.as_view(), name='login-refresh'),   
]


