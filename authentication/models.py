from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _ 
import uuid
from django.conf import settings
# Create your models here.

from .manager import CustomUserManager


class Hostel(models.Model):
    
    GENDER = (
        ("male", "male"),
        ("female", "female")
    )
    
    HOSTELS = (
        ("Professor Biobaku Hall", "Professor Biobaku Hall"),
        ("Queen Amina Hall", "Queen Amina Hall"),
        ("King Jaja Hall", "King Jaja hall"),
        ("Osun block", "Osun block"),
        ("Ondo block", "Ondo block"),
        ("Calabar block", "Calabar block"),
        ("Anthony block", "Anthony block"),
        ("Ekiti block", "Ekiti block"),
        ("Oyo block", "Oyo block"),
        ("Kwara block", "Kwara block"),
        ("Kogi block", "Kogi block"),
        ("Block A", "Block A"),
        ("Block B", "Block B"),
        ("Block C", "Block C"),
        ("Block D", "Block D"),
        ("Block NH", "Block NH"),
        ("Block AKB", "Block AKB"),
        ("Block AKB Anex", "Block AKB Anex"),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, choices=HOSTELS)
    no_of_rooms = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER)
    
    
    def __str__(self) -> str:
        return self.name 


 
class CustomUser(AbstractUser):
    username = None 
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, max_length=6)
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=50) 
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10, choices=Hostel.GENDER)
    matric_number = models.CharField(max_length=11, unique=True, null=True)
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, null=True)
    is_student = models.BooleanField(default=False)
    is_porter = models.BooleanField(default=False)
    
    
    USERNAME_FIELD = 'matric_number' 
    REQUIRED_FIELDS = ["first_name", "last_name", "email"]
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email 
       

class StudentUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    faculty = models.CharField(max_length=100, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    room_no = models.CharField(max_length=5, null=True)
    block_no = models.CharField(max_length=5, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.matric_number


class PorterUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.email