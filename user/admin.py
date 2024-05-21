from django.contrib import admin
from .models import CustomUser

# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'user_id', 'job', 'user_no')
    
admin.site.register(CustomUser,CustomUserAdmin)