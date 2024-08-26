from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Hotel)
admin.site.register(User)

admin.site.register(EmployeePost)
admin.site.register(EmployeeInfo)
admin.site.register(Department)
admin.site.register(AttendanceDate)
admin.site.register(Attendance)
admin.site.register(Shift)
admin.site.register(EmployeeShift)

