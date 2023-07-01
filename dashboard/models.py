from django.db import models
from authentication.models import StudentUser
import uuid 
# Create your models here.



class Complaint(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    student = models.ForeignKey(StudentUser, on_delete=models.CASCADE, related_name='complaints', null=True, blank=True)
    hostel = models.CharField(max_length=100, null= True)
    date_filed = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)
    
    def __str__(self):
        return self.student.user.first_name 


    