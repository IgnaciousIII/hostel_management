from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_warden = models.BooleanField(default=False)


class Student(models.Model):
    user = models.OneToOneField(
        User,
        default=None,
        null=True,
        on_delete=models.CASCADE)
    gender_choices = [('M', 'Male'), ('F', 'Female')]
    student_name = models.CharField(max_length=200, null=True)
    father_name = models.CharField(max_length=200, null=True)
    enrollment_no = models.CharField(max_length=10, unique=True, null=True)
    course = models.ForeignKey(
        'Course',
        null=True,
        default=None,
        on_delete=models.CASCADE)
    dob = models.DateField(
        max_length=10,
        help_text="format : YYYY-MM-DD",
        null=True)
    gender = models.CharField(
        choices=gender_choices,
        max_length=1,
        default=None,
        null=True)
    room = models.OneToOneField(
        'Room',
        blank=True,
        on_delete=models.CASCADE,
        null=True)
    room_allotted = models.BooleanField(default=False)
    no_dues = models.BooleanField(default=True)

    def __str__(self):
        return self.student_name or "Unnamed Student"


class Room(models.Model):
    room_choice = [('S', 'Single Occupancy'), ('D', 'Double Occupancy'), ('P', 'Reserved for Research Scholars'),('B', 'Both Single and Double Occupancy')]
    no = models.CharField(max_length=5)
    name = models.CharField(max_length=10)
    room_type = models.CharField(choices=room_choice, max_length=1, default=None)
    vacant = models.BooleanField(default=False)
    hostel = models.ForeignKey('Hostel', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Hostel(models.Model):
    name = models.CharField(max_length=5)
    gender_choices = [('M', 'Male'), ('F', 'Female')]
    gender = models.CharField(
        choices=gender_choices,
        max_length=1,
        default=None,
        null=True)
    course = models.ManyToManyField('Course', default=None, blank=True)
    caretaker = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    # if a student has enrollment number iit2017001 then the course code is iit2017
    code = models.CharField(max_length=100, default=None)
    room_choice = [('S', 'Single Occupancy'), ('D', 'Double Occupancy'), ('P', 'Reserved for Research Scholars'), ('B', 'Both Single and Double Occupancy')]
    room_type = models.CharField(choices=room_choice, max_length=1, default='D')

    def __str__(self):
        return self.code


class Warden(models.Model):
    user = models.OneToOneField(
        User,
        default=None,
        null=True,
        on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    hostel = models.ForeignKey('Hostel',
        default=None,
        null=True,
        on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# models.py

from django.db import models


class Fee(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('Online', 'Online'),
        ('Cash', 'Cash'),
        ('UPI', 'UPI'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming you use User model for students
    due_amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    payment_status = models.BooleanField(default=False)  # True for paid, False for due
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES, default='Online')
    payment_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.student.username} Fee Details'
# models.py

# models.py

class Visitor(models.Model):
    warden = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)  # Assuming Warden is a User
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="visitors")  # Student being visited
    visitor_name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=100)
    visit_date = models.DateField()
    visit_time = models.TimeField()
    purpose = models.TextField()

    def __str__(self):
        return f'Visitor {self.visitor_name} for {self.student.username}'


# models.py

class Attendance(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming you use User model for students
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')], default='Present')
    remarks = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.student.username} - Attendance for {self.date}'

# models.py

class Complaint(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming you use User model for students
    complaint_text = models.TextField()
    date_filed = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Resolved', 'Resolved')], default='Pending')
    remarks = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f'Complaint by {self.student.username} - Status: {self.status}'
