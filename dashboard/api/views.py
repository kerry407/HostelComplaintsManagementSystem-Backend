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
from authentication.models import StudentUser

class ComplaintsViewSet(viewsets.ModelViewSet):
    serializer_class = ComplaintSerializer
    queryset = Complaint.objects.all()
    search_fields = ["title", "student"]
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
        
    
class StudentViewSet(viewsets.ModelViewSet):
    queryset = StudentUser.objects.all()
    serializer_class = StudentDashBoardSerializer 
    permission_classes = [IsAdminOrReadOnly]
    renderer_classes = [CustomRenderer]
    
class PorterViewSet(viewsets.ModelViewSet):
    queryset = PorterUser.objects.all()
    serializer_class = PorterDashBoardSerializer
    permission_classes = [IsAdminOrReadOnly]
    renderer_classes = [CustomRenderer]


class DashBoardCountView(AutoPrefetchViewSetMixin, views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [CustomRenderer]
    
    def get(self, request):
        student_count = StudentUser.objects.filter(user__hostel=request.user.hostel).count()
        porter_count = PorterUser.objects.filter(user__hostel=request.user.hostel).count()
        complaints_count = Complaint.objects.filter(student__user__hostel=request.user.hostel).count()
        return Response(
            {
                "student_count": student_count,
                "porter_count": porter_count,
                "complaints_count": complaints_count
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
    