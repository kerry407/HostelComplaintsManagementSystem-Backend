from django.contrib import admin
from .models import Complaint
# Register your models here.

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "student", "date_filed", "is_resolved")
    