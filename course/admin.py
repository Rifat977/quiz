from django.contrib import admin
from .models import Course

# Register your models here.
class CourseDisplay(admin.ModelAdmin):
    list_display = ('name','slug', 'status')
    search_fields  = ('name','slug', 'status')

admin.site.register(Course, CourseDisplay)