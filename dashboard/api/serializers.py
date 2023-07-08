from rest_framework import serializers
from ..models import Complaint 
from authentication.models import StudentUser, PorterUser, Hostel      
        
class ComplaintSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField()
    student_first_name = serializers.SerializerMethodField()
    student_last_name = serializers.SerializerMethodField()
    student_room_no = serializers.SerializerMethodField()
    student_block_no = serializers.SerializerMethodField()
    hostel = serializers.StringRelatedField()
    
    def get_student_first_name(self, obj):
        return obj.student.user.first_name
    
    def get_student_last_name(self, obj):
        return obj.student.user.last_name
    
    def get_student_room_no(self, obj):
        return obj.student.room_no
    
    def get_student_block_no(self, obj):
        return obj.student.block_no
    
    class Meta:
        model = Complaint 
        fields = "__all__"
        

class StudentDashBoardSerializer(serializers.ModelSerializer):
    students_details = serializers.SerializerMethodField()
    
    def get_students_details(self, obj):
        students = StudentUser.objects.filter(user__hostel=obj.user.hostel).count()
        student_complaint = Complaint.objects.filter(student=obj)
        all_complaints = student_complaint.count()
        resolved_complaints = student_complaint.filter(is_resolved=True).count()
        unresolved_complaint = student_complaint.filter(is_resolved=False).count()
        details_dict = {}
        try:
            details_dict["matric_number"] = obj.user.matric_number
            details_dict["email"] = obj.user.email 
            details_dict["first_name"] = obj.user.first_name 
            details_dict["last_name"] = obj.user.last_name 
            details_dict["hostel"] = obj.user.hostel.name
            details_dict["number_of_students_in_hostel"] = students
            details_dict["all_complaints"] = all_complaints
            details_dict["resolved_complaints"] = resolved_complaints
            details_dict["unresolved_complaint"] = unresolved_complaint
        except KeyError as e:
            raise(e)
        except AttributeError:
            raise serializers.ValidationError("object has no hostel")
        return details_dict
    
    class Meta:
        model = StudentUser 
        fields = "__all__"
        
class PorterDashBoardSerializer(serializers.ModelSerializer):
    porter_details = serializers.SerializerMethodField()
    
    def get_porter_details(self, obj):
        porters = PorterUser.objects.filter(user__hostel=obj.user.hostel).count()
        students = StudentUser.objects.filter(user__hostel=obj.user.hostel).count()
        student_complaint = Complaint.objects.filter(hostel=obj.user.hostel)
        all_complaints = student_complaint.count()
        resolved_complaints = student_complaint.filter(is_resolved=True).count()
        unresolved_complaint = student_complaint.filter(is_resolved=False).count()
        details_dict = {}
        details_dict["email"] = obj.user.email 
        details_dict["first_name"] = obj.user.first_name 
        details_dict["last_name"] = obj.user.last_name 
        details_dict["hostel"] = obj.user.hostel.name
        details_dict["number_of_students_in_hostel"] = students
        details_dict["number_of_porters_in_hostel"] = porters 
        details_dict["all_complaints"] = all_complaints
        details_dict["resolved_complaints"] = resolved_complaints
        details_dict["unresolved_complaint"] = unresolved_complaint
        return details_dict 
    
    class Meta:
        model = PorterUser 
        fields = "__all__"
        

class HostelSerializer(serializers.ModelSerializer):
    complaint_by_hostel = serializers.SerializerMethodField()
    
    def get_complaint_by_hostel(self, obj):
        complaints = Complaint.objects.filter(hostel=obj).count()
        return complaints
    
    class Meta:
        model = Hostel
        fields = "__all__"