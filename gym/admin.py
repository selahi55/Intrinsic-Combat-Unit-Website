from django.contrib import admin
from .models import Course, Schedule, Video

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['course', 'time', 'day']

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['caption', 'videofile']