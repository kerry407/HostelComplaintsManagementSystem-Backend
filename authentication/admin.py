from django.contrib import admin

# Register your models here.
from .models import CustomUser, StudentUser, PorterUser, Hostel

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email','first_name', 'last_name', 'is_student', 'is_porter', 'is_staff', 'is_active')
    list_filter = ('email', 'is_staff', 'is_active')
    search_fields = ('email',)
    ordering = ('email',)
    
@admin.register(StudentUser)
class StudentUserAdmin(admin.ModelAdmin):
    pass
    
@admin.register(PorterUser)
class PorterUserAdmin(admin.ModelAdmin):
    pass

@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    list_display = ["name", "no_of_rooms", "gender"]





