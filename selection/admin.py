from django.contrib import admin
from .models import Student, Room, Hostel, Course, User, Warden


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'student_name',
        'father_name',
        'gender',
        'enrollment_no',
        'course',
        'dob',
        'room',
        'room_allotted'
    ]


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['no', 'name', 'room_type', 'vacant', 'hostel']


@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    list_display = ['name', 'gender']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'room_type']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):  # Corrected class name
    list_display = ['is_warden']


@admin.register(Warden)
class WardenAdmin(admin.ModelAdmin):  # Corrected class name
    list_display = ['name']

# admin.py

from django.contrib import admin
from .models import Fee, Visitor, Attendance, Complaint

@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ['student', 'due_amount', 'due_date', 'payment_status', 'payment_method', 'payment_date']


@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ['warden', 'student', 'visitor_name', 'relationship', 'visit_date', 'visit_time', 'purpose']


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'date', 'status', 'remarks']

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['student', 'complaint_text', 'date_filed', 'status', 'remarks']

class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['student', 'complaint_text', 'date_filed', 'status', 'remarks']
    actions = ['mark_as_resolved']

    def mark_as_resolved(self, request, queryset):
        queryset.update(status='Resolved')
    mark_as_resolved.short_description = 'Mark selected complaints as resolved'