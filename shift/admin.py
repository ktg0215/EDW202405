from django.contrib import admin
from .models import Schedule

# class ScheduleAdmin(admin.ModelAdmin):
#     )
#     list_display = ('shops','date')


admin.site.register(Schedule)
