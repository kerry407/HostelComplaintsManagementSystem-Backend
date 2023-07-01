from ..models import *
from rest_framework import serializers
from rest_framework_simplejwt.serializers import PasswordField, TokenObtainPairSerializer


class AccountSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    hostel_name = serializers.SerializerMethodField()
    
    def get_hostel_name(self, obj):
        return obj.hostel.name
    
    class Meta:
        model = CustomUser 
        fields = ["id", "first_name", "last_name", "matric_number", "email", "hostel", "gender", "hostel_name", "password", "password2"]
        extra_kwargs = {
            "password": {"write_only": True}
        }
        
    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("The two passwords do not match !")
        data.pop("password2")
        return data 
    
    def create(self, validated_data):
        email = validated_data["email"]
        confirm_account = CustomUser.objects.filter(email=email)
        if confirm_account.exists():
            raise serializers.ValidationError("An account already exists with this email")
        new_account = CustomUser.objects.create_user(**validated_data)
        return new_account
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    

class StudentTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['matric_number'] = serializers.CharField(required=True)
        self.fields['password'] = PasswordField(trim_whitespace=False)
        CustomUser.USERNAME_FIELD = "matric_number"
        self.username_field = 'matric_number'
        
    def validate(self, attrs):
        data = super().validate(attrs)
        data.update(
            {
                "id": self.user.id,
                "email": self.user.email,
                "matric_number": self.user.matric_number,
                "first_name": self.user.first_name,
                "last_name": self.user.last_name,
                "hostel": self.user.hostel.name,
                "is_student": self.user.is_student,
                "is_porter": self.user.is_porter,
                "is_superuser": self.user.is_superuser,
                "is_staff": self.user.is_staff,
            }
        )
        return data
    
    
class PorterTokenObtainPairSerializer(TokenObtainPairSerializer):   
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'] = serializers.CharField(required=True)
        self.fields['password'] = PasswordField(trim_whitespace=False)
        CustomUser.USERNAME_FIELD = "email"
        self.username_field = 'email'
    
    
    def validate(self, attrs):
        data = super().validate(attrs)
        if self.user.is_student:
            raise serializers.ValidationError("Students not allowed!")
        data.update(
            {
                "id": self.user.id,
                "email": self.user.email,
                "matric_number": self.user.matric_number,
                "first_name": self.user.first_name,
                "last_name": self.user.last_name,
                "hostel": self.user.hostel.name,
                "is_student": self.user.is_student,
                "is_porter": self.user.is_porter,
                "is_superuser": self.user.is_superuser,
                "is_staff": self.user.is_staff,
            }
        )
        return data
        

class StudentSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = StudentUser
        fields = "__all__"
        
class PorterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PorterUser
        fields = "__all__"
        
        

