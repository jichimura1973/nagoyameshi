from django.contrib import admin
# from .models import CustomUser, Job
from .models import CustomUser, Job

class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name_kanji', 'job', 'gender')
    search_fields = ('user_name_kanji', 'job', 'gender')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Job, JobAdmin)
# admin.site.register(Job)


