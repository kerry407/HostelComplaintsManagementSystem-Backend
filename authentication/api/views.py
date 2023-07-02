from rest_framework import generics, permissions, status, validators
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from ..models import *
from .serializers import AccountSerializer, ChangePasswordSerializer
from dashboard.api.renderers import CustomRenderer
from dashboard.api.permissions import CustomPermissions
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (
StudentTokenObtainPairSerializer, 
PorterTokenObtainPairSerializer,
)


class AccountCreateView(generics.CreateAPIView):
    '''
        API endpoint for creating an account 
    '''
    serializer_class = AccountSerializer
    permission_classes = [permissions.AllowAny]
    renderer_classes = [CustomRenderer]
    
    def perform_create(self, serializer):
        if "matric_number" in self.request.data:
            serializer.save(
                            is_student=True
                            ) 
        else:
            serializer.save(
                            is_porter=True
                            )
        
class AccountDetailsView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [CustomPermissions]
    serializer_class = AccountSerializer
    renderer_classes = [CustomRenderer]
    
    def perform_update(self, serializer):
        if "password" in self.request.data:
            raise validators.ValidationError(
                {"error": "Not Allowed"}
            )
        else:
            serializer.save()
            
class AccountsListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AccountSerializer 
    renderer_classes = [CustomRenderer]
            

class ChangePasswordView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        old_password = request.data.get("old_password")
        if not request.user.check_password(old_password):
            return Response({"error": "Incorrect password"}, status=status.HTTP_400_BAD_REQUEST)
        
        new_password = request.data.get("new_password")
        request.user.set_password(new_password)
        request.user.save()
        
        return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)
  
  
    
class StudentTokenObtainPairViewSet(TokenObtainPairView):
    """
    Endpoint for Student Login
    """
    serializer_class = StudentTokenObtainPairSerializer
    
    
class PorterTokenObtainPairViewSet(TokenObtainPairView):
    """
    Endpoint for Porter Login
    """
    serializer_class = PorterTokenObtainPairSerializer
    
    

