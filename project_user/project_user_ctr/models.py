from django.db import models
from django.contrib.auth.models import User

class Register(models.Model):
    full_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    mobile_no = models.CharField(max_length=10, unique=True)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    course = models.CharField(max_length=255)
    reg_no = models.CharField(max_length=50, unique=True)
    ac_year = models.CharField(max_length=4)
    course_year = models.CharField(max_length=4)
    password = models.CharField(max_length=100)

    class Meta:
        db_table = "register"  


class HostelApp(models.Model):
    user = models.OneToOneField(Register, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, default='N/A')
    father_name = models.CharField(max_length=100, default='N/A')
    mobile_no = models.CharField(max_length=10, default='0000000000')
    email = models.EmailField(default='example@example.com')
    address = models.CharField(max_length=255, default='N/A')
    institution = models.CharField(max_length=255, default='N/A')
    course = models.CharField(max_length=255, default='N/A')
    reg_no = models.CharField(max_length=50, default='N/A')
    ac_year = models.CharField(max_length=4, default='2024')
    course_year = models.CharField(max_length=4, default='1')
    photo = models.ImageField(upload_to='photos/', null=False)
    number_of_sharing = models.IntegerField(null=False)
    mother_name = models.CharField(max_length=20, null=False, blank=True)
    occupation = models.CharField(max_length=20, null=False, blank=True)
    landline_num = models.CharField(max_length=20, null=False, blank=True)
    emergency_contact = models.CharField(max_length=15, null=False, blank=True)
    father_email = models.EmailField(max_length=50, null=False, blank=True)
    applied_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')


class ComplaintBox(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    register_number = models.CharField(max_length=20)
    subject = models.CharField(max_length=50)
    complaint = models.TextField()
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"{self.name} - {self.subject}"


class RoomAllot(models.Model):
    floor = models.CharField(max_length=10)
    room_number = models.CharField(max_length=10)
    number_of_entries = models.IntegerField(default=1)
    name = models.CharField(max_length=100)
    usn = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} ({self.usn}) - Room {self.room_number}, Floor {self.floor}"

class AdminLog(models.Model):
    user_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    
    def __str__(self):
        return self.user_name


class Notice(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


