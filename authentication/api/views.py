from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status 
from django.contrib.auth.hashers import make_password



from django.contrib.auth import get_user_model
from ..models import *
from .serializers import AccountSerializer, ChangePasswordSerializer
from dashboard.api.renderers import CustomRenderer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (
StudentTokenObtainPairSerializer, 
PorterTokenObtainPairSerializer,
StudentSerializer,
PorterSerializer
)


class AccountCreateView(generics.CreateAPIView):
    '''
        API endpoint for creating an account 
    '''
    serializer_class = AccountSerializer
    permission_classes = [AllowAny]
    renderer_classes = [CustomRenderer]
    
    def perform_create(self, serializer):
        super().perform_create(serializer)
        if "matric_number" in self.request.data:
            serializer.save(
                            is_student=True, 
                            password=make_password(serializer.validated_data["password"])
                            ) 
        else:
            serializer.save(
                            is_porter=True, 
                            password=make_password(serializer.validated_data["password"])
                            )
        
            

class ChangePasswordView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

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
    serializer_class = StudentTokenObtainPairSerializer
    
    
class PorterTokenObtainPairViewSet(TokenObtainPairView):
    serializer_class = PorterTokenObtainPairSerializer