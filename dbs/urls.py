from django.contrib import admin
from django.urls import path
import debug_toolbar
from django.urls import path, include
from selection import views
from selection.views import log_visitor
from selection.views import file_complaint, view_complaints, view_attendance, mark_attendance

urlpatterns = [
    path('admin/', admin.site.urls),
    path('file_complaint/', views.file_complaint, name='file_complaint'),
    path('', views.home, name='register'),
    path('complaint_success/', views.complaint_success, name='complaint_success'),
    path("mark_attendance/", mark_attendance, name="mark_attendance"),
    path('visitor/<int:student_id>/', views.log_visitor, name='log_visitor'),
    path('reg_form/', views.register, name='reg_form'),
    path('student/complaint/', file_complaint, name='file_complaint'),
    path('student/complaints/', view_complaints, name='view_complaints'),
    path('student/attendance/', view_attendance, name='view_attendance'),
    path('login/', views.user_login, name='login'),
    path('warden_login/', views.warden_login, name='warden_login'),
    path('warden_dues/', views.warden_dues, name='warden_dues'),
    path('warden/complaints/', views.view_complaints, name='view_complaints'),
    path('warden/visitor/', views.log_visitor, name='log_visitor'),
    path('warden/visitor/', log_visitor, name='log_visitor'),
    path('warden/file_complaint/', views.file_complaint, name='file_complaint'),
    path('warden_add_due/', views.warden_add_due, name='warden_add_due'),
    path("warden/mark_attendance/", mark_attendance, name="mark_attendance"),
    path('warden_remove_due/', views.warden_remove_due, name='warden_remove_due'),
    path('hostels/<slug:hostel_name>/', views.hostel_detail_view, name='hostel'),
    path('login/edit/', views.edit, name='edit'),
    path('login/select/', views.select, name='select'),
    path('logout/', views.logout_view, name='logout'),
    path('warden/visitor/success/', views.visitor_success, name='visitor_log_success'),
    path('reg_form/login/edit/', views.edit, name='update'),
    path('__debug__/', include(debug_toolbar.urls)),
 
]