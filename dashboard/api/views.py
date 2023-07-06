from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import (
    viewsets,
    permissions,
    generics,
    serializers,
    validators,
    views,
    status
)
from rest_framework.response import Response 
from django_auto_prefetching import AutoPrefetchViewSetMixin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from .serializers import *
from .renderers import CustomRenderer
from ..filters import ComplaintFilter
from .permissions import CustomPermissions, IsAdminOrReadOnly
from authentication.models import StudentUser, Hostel

class ComplaintsViewSet(AutoPrefetchViewSetMixin, viewsets.ModelViewSet):
    """
    Endpoint for Complaints (All CRUD actions)
    """
    serializer_class = ComplaintSerializer
    queryset = Complaint.objects.all()
    search_fields = ["title", "student__user__first_name", "student__user__last_name"]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ComplaintFilter
    renderer_classes = [CustomRenderer]
    
    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Complaint.objects.none()
        return super().get_queryset().filter(hostel=self.request.user.hostel)
        

    def get_permissions(self):
        
        if self.action == "create":
            self.permission_classes = [permissions.IsAuthenticated]  
        elif self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes = [CustomPermissions]
        else:
            self.permission_classes = [permissions.AllowAny]
            
        return super().get_permissions()
    
    def perform_create(self, serializer):
        # Assign users with is_instructor field to create courses
        if not self.request.user.is_student:
            raise validators.ValidationError(
                                            {
                                            "detail": "User must have is_student = True to create a complaint"
                                            }
                                            )
        student = get_object_or_404(StudentUser, user=self.request.user)
        serializer.save(student=student, hostel=student.user.hostel)
        
    
class StudentViewSet(AutoPrefetchViewSetMixin, viewsets.ModelViewSet):
    """
    Endpoint for accessing all students (All CRUD actions)
    """
    queryset = StudentUser.objects.all()
    serializer_class = StudentDashBoardSerializer 
    renderer_classes = [CustomRenderer]
    
    def get_queryset(self):
        param = self.request.query_params.get("hostel")
        user = self.request.user
        if not user.is_anonymous:
            return super().get_queryset().filter(user__hostel__name=user.hostel.name)
        elif param:
            return super().get_queryset().filter(user__hostel__name=param)
        return super().get_queryset()
    
    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [permissions.IsAuthenticated]
        if self.action in ["list", "retreive"]:
            self.permission_classes = [permissions.AllowAny]
        if self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes = [CustomPermissions]
            
        return super().get_permissions()
    
class PorterViewSet(AutoPrefetchViewSetMixin, viewsets.ModelViewSet):
    """
    Endpoint for accessing all porters (All CRUD activites)
    """
    queryset = PorterUser.objects.all()
    serializer_class = PorterDashBoardSerializer
    renderer_classes = [CustomRenderer]
    
    def get_queryset(self):
        param = self.request.query_params.get("hostel")
        user = self.request.user
        if not user.is_anonymous:
            return super().get_queryset().filter(user__hostel__name=user.hostel.name)
        elif param:
            return super().get_queryset().filter(user__hostel__name=param)
        return super().get_queryset()
    
    
    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [permissions.IsAuthenticated]
        if self.action in ["list", "retreive"]:
            self.permission_classes = [permissions.AllowAny]
        if self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes = [CustomPermissions]

        return super().get_permissions()

class DashBoardCountView(AutoPrefetchViewSetMixin, views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [CustomRenderer]
    
    def get(self, request):
        student_count = StudentUser.objects.filter(user__hostel=request.user.hostel).count()
        porter_count = PorterUser.objects.filter(user__hostel=request.user.hostel).count()
        complaints_count = Complaint.objects.filter(student__user__hostel=request.user.hostel).count()
        hostel_room_count = request.user.hostel.no_of_rooms
        hostel_gender = request.user.hostel.gender
        
        return Response(
            {
                "student_count": student_count,
                "porter_count": porter_count,
                "complaints_count": complaints_count,
                "hostel_room_count": hostel_room_count,
                "hostel_gender": hostel_gender
            },
            status=status.HTTP_200_OK
        )
        

class HostelViewSet(viewsets.ModelViewSet):
    queryset = Hostel.objects.all()
    serializer_class = HostelSerializer 
    renderer_classes = [CustomRenderer]
        
    def get_permissions(self):
          
        if self.action in ["create", "update", "partial_update", "destroy"]:
            self.permission_classes = [permissions.IsAdminUser]
        else:
            self.permission_classes = [permissions.AllowAny]
            
        return super().get_permissions()
    