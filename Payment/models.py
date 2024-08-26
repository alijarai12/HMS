from django.db import models
from Authentication.models import Hotel
from Employee.models import *
from Guest.models  import Guest

# Create your models here.
class PaymentMethod(models.Model):
    name = models.CharField(max_length=300)
    payment_detail = models.CharField(max_length=300)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at']

class BankInfo(models.Model):
    bank_name = models.CharField(max_length=300)
    bank_branch = models.CharField(max_length=300)
    bank_account_no = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE)

    def __str__(self):
        return self.bank_name
    
    class Meta:
        ordering = ['-created_at']
    
class Transaction(models.Model):
    payment_status = (('Paid', 'Paid'),('Not paid','Not paid'))
    confirmed_by = models.ForeignKey(EmployeeInfo, on_delete=models.CASCADE,null=True)
    guest =models.ForeignKey(Guest,on_delete=models.CASCADE,null=True)
    total = models.FloatField(default=0.00,null=True)
    status = models.CharField(choices=payment_status, default='Not paid', max_length=300)
    received_amount = models.FloatField(default=0.00,null=True)
    service_fee = models.FloatField(default=0.00,null=True)
    discount = models.FloatField(default=0.00,null=True)
    discount_reason =models.CharField(max_length=30)
    change_returned =models.FloatField(default=0.00,null=True)
    payment_method=models.ForeignKey(PaymentMethod,null=True,blank=True, on_delete=models.CASCADE)
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return (str(self.guest))
    

