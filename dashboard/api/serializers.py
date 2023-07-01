from rest_framework import serializers
from ..models import Complaint 
from authentication.models import StudentUser, PorterUser, Hostel
from django.shortcuts import get_object_or_404       
        
class ComplaintSerializer(serializers.ModelSerializer):

    class Meta:
        model = Complaint 
        fields = "__all__"
        

class StudentDashBoardSerializer(serializers.ModelSerializer):
    students_details = serializers.SerializerMethodField()
    
    def get_students_details(self, obj):
        students = StudentUser.objects.filter(user__hostel=obj.user.hostel).count()
        details_dict = {}
        details_dict["matric_number"] = obj.user.matric_number
        details_dict["email"] = obj.user.email 
        details_dict["first_name"] = obj.user.first_name 
        details_dict["last_name"] = obj.user.last_name 
        details_dict["hostel"] = obj.user.hostel.name
        details_dict["number_of_students_in_hostel"] = students
        return details_dict
    
    class Meta:
        model = StudentUser 
        fields = "__all__"
        
class PorterDashBoardSerializer(serializers.ModelSerializer):
    porter_details = serializers.SerializerMethodField()
    
    def get_porter_details(self, obj):
        porters = PorterUser.objects.filter(user__hostel=obj.user.hostel).count()
        students = StudentUser.objects.filter(user__hostel=obj.user.hostel).count()
        details_dict = {}
        details_dict["email"] = obj.user.email 
        details_dict["first_name"] = obj.user.first_name 
        details_dict["last_name"] = obj.user.last_name 
        details_dict["hostel"] = obj.user.hostel.name
        details_dict["number_of_students_in_hostel"] = students
        details_dict["number_of_porters_in_hostel"] = porters 
        return details_dict 
    
    class Meta:
        model = PorterUser 
        fields = "__all__"
        

class HostelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Hostel
        fields = "__all__"