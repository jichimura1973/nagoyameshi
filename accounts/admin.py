from django.contrib import admin
# from .models import CustomUser, Job
from .models import CustomUser, Job, MonthlySales

class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

class MonthlySalesAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'sales')
    
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name_kanji', 'job', 'gender', 'updated_day')
    search_fields = ('user_name_kanji', 'job', 'gender')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(MonthlySales, MonthlySalesAdmin)
# admin.site.register(Job)


