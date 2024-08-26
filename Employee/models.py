from django.db import models
from Authentication.models import User, Hotel
from django.contrib.auth.models import Group
# Create your models here.

gender_choices = [('Male','Male'),('Female','Female'),('Others','Others')]
day_choices = [('Sunday','Sunday'),('Monday','Monday'),('Tuesday','Tuesday'),('Wednesday','Wednesday'),('Thursday','Thursday'),('Friday','Friday'),('Saturday','Saturday')]

class EmployeePost(models.Model):
    post_name = models.CharField(max_length=300)
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='employeeposts') 
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)  

    class Meta:
        ordering = ['-created_date']


    def __str__(self):
        return self.post_name



class EmployeeInfo(models.Model):
    CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),
    ]
    # Groups = [
    #     ('Manager','Manager'),
    #     ('Waiter','Waiter'),
    #     ('Counter','Counter'),
    #     ('Kitchen','Kitchen')
    # ]
    first_name = models.CharField(max_length=300)
    middle_name = models.CharField(max_length=300, null=True, blank=True)
    last_name = models.CharField(max_length=300)
    contact = models.BigIntegerField(unique=True)
    pan_no = models.CharField(max_length=300,null=True)
    permanent_address = models.CharField(max_length=300)
    current_address = models.CharField(max_length=300)
    gender = models.CharField(max_length=300, choices=CHOICES)    
    email = models.EmailField(unique=True)
    join_date = models.DateField()
    photo = models.ImageField(upload_to='employee_image', null=True, blank=True)
    cv = models.FileField(upload_to='employee_cv_file', null=True, blank=True)
    bank_account_no = models.CharField(max_length=300)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='employeeinfos')
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='employeeinfos')
    department = models.ForeignKey('Department', on_delete=models.CASCADE, related_name='employeeinfos')
    post = models.ForeignKey(EmployeePost, on_delete=models.CASCADE, related_name='employeeinfos')
    employee_role = models.ForeignKey(Group,on_delete=models.SET_NULL,null=True)
    salary = models.FloatField(default=0.0)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-created_date']
    
    def __str__(self):
        full_name = f'{self.first_name} '
        if self.middle_name:
            full_name += f'{self.middle_name} '
        full_name += self.last_name
        return full_name
    


class Department(models.Model):
    dept_name = models.CharField(max_length=300)
    manager_name = models.OneToOneField(EmployeeInfo, on_delete=models.CASCADE, blank=True, null=True, related_name='departments')
    contact = models.CharField(max_length=300)
    description = models.TextField(default='')
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='departments')
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.dept_name


class AttendanceDate(models.Model):
    date = models.DateField()
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='attendancedates')
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return str(self.date)


class Attendance(models.Model):
    employee = models.ForeignKey(EmployeeInfo, on_delete=models.CASCADE, related_name='attendances')
    attendance_date = models.ForeignKey(AttendanceDate, on_delete=models.CASCADE, default=True, related_name='attendances')  # Updated field name and related name
    check_in_time = models.DateTimeField(auto_now_add=True)
    check_out_time = models.DateTimeField(auto_now_add=True)
    present = models.BooleanField(default=False)
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='attendances')
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-created_date'] 


    def __str__(self):
        return str(self.attendance_date)
    
    
class Shift(models.Model):
    shift_name = models.CharField(max_length=300)
    day = models.CharField(max_length=50,choices=day_choices)
    starting_time = models.TimeField()
    ending_time = models.TimeField()
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='shifts')
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.shift_name
    
class EmployeeShift(models.Model):
    shift_name = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name='employeeshifts')
    date = models.DateField(auto_now_add=True)
    employee = models.ForeignKey(EmployeeInfo, on_delete=models.CASCADE, related_name='employeeshifts')
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='employeeshifts')
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return str(self.shift_name)
    

    
