from django.db import models
from Authentication .models import *
from Guest .models import *
# Create your models here.

status = (('Active', 'Active'), ('Inactive', 'Inactive'))
spapackagetype = (('massages', 'massages'), ('facials', 'facials'), ('bodywraps', 'bodywraps'), ('steambaths', 'steambaths'))
payment_choices = (('Paid', 'Paid'), ('Unpaid', 'Unpaid'))
class Gym(models.Model):
    gym_name = models.CharField(max_length=200)
    gym_contact = models.CharField(max_length=200)
    gym_capacity = models.IntegerField()
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.gym_name


class GymPackages(models.Model):
    package_name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=200)
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.package_name
    
class GymMember(models.Model):
    guest_id = models.ForeignKey(Guest, on_delete=models.CASCADE, null=True)
    is_guest = models.BooleanField(default=False)
    member_id = models.ForeignKey(Membership, on_delete=models.CASCADE,null=True)
    gym_packages_id = models.ForeignKey(GymPackages, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    status = models.CharField(max_length=200, choices=status, default='Inactive')   
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    def __str__(self):
        return str(self.guest_id)

class GymFeedback(models.Model):
    date = models.DateField(auto_now_add=True)
    comment = models.CharField(max_length=200)
    gym_member = models.ForeignKey(GymMember, on_delete=models.CASCADE)
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
class GymAttendance(models.Model):
    date_time = models.DateTimeField(auto_now_add=True)
    gym_member = models.ForeignKey(GymMember, on_delete=models.CASCADE)    
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE)    
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

class NutritionPlan(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    dailymealplan = models.CharField(max_length=200)
    gym_member = models.ForeignKey(GymMember, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
class GymInvoice(models.Model):
    gym_member = models.ForeignKey(GymMember, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)   

#Spa Model

class Spa(models.Model):
    spa_name = models.CharField(max_length=200)
    spa_contact = models.CharField(max_length=200)
    capacity = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE,null=True)
       
class SpaMember(models.Model):
    guest_id = models.ForeignKey(Guest, on_delete=models.CASCADE)
    is_guest = models.BooleanField(default=False)
    member_id = models.ForeignKey(Membership, on_delete=models.CASCADE)
    spa_package = models.ForeignKey("SpaPackage", on_delete=models.CASCADE,null=True)
    status = models.CharField(max_length=50,choices=status,null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE,null=True)

class SpaPackage(models.Model):
    packagetype = models.CharField(max_length=200, choices=spapackagetype)
    description = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=300,null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE,null=True)
    
class SpaService(models.Model):
    service_name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    package = models.ForeignKey(SpaPackage,on_delete=models.SET_NULL,null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE,null=True)
    
class SpaFeedback(models.Model):
    date = models.DateField(auto_now_add=True)
    comment = models.CharField(max_length=200)
    spamember_id = models.ForeignKey(SpaMember, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE,null=True)
    
class SpaBooking(models.Model):
    customername = models.CharField(max_length=200)
    dateandtime = models.DateTimeField(auto_now_add=True)
    duration = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=200, choices=payment_choices, default="Unpaid")
    contact_no = models.CharField(max_length=200)
    service_id = models.ForeignKey(SpaService, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)   
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE,null=True)
    
class SpaInvoice(models.Model):
    spa_member = models.ForeignKey(SpaMember, on_delete=models.CASCADE)
    spa_booking = models.ForeignKey(SpaBooking, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE,null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)       
