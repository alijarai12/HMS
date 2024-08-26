from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import EmployeeInfo

@receiver(post_save, sender=User)
def update_employee_info(sender, instance, **kwargs):
    # instance is the User instance
    print(instance.email)
    try:
        employee_info = instance.employeeinfos
        employee_info.email = instance.email
        employee_info.save()
    except EmployeeInfo.DoesNotExist:
        pass
