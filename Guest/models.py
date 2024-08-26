from django.db import models
from Employee.models import *
from Authentication.models import Hotel


class OrganizationType(models.Model):
    org_type_name = models.CharField(max_length=300)
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='organizationtypes')
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.org_type_name


class Organization(models.Model):
    organization_name = models.CharField(max_length=300)
    organization_type = models.ForeignKey(OrganizationType, on_delete=models.CASCADE, related_name='organizations')
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.organization_name


class GuestType(models.Model):
    guest_type_name = models.CharField(max_length=300)
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='guest_types')
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.guest_type_name

class Guest(models.Model):
    first_name = models.CharField(max_length=300)
    middle_name = models.CharField(max_length=300,null=True, blank=True)
    last_name = models.CharField(max_length=300)
    address = models.CharField(max_length=300)
    phone = models.CharField(max_length=300)
    email = models.EmailField(unique=True)
    guest_type = models.ForeignKey(GuestType, on_delete=models.CASCADE, related_name='guests')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True, related_name='guests')
    is_available = models.BooleanField(default=True)
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='guests')
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-created_date']
    
    
    def __str__(self):
        if self.middle_name:
            return f'{self.first_name.title()} {self.middle_name.title()} {self.last_name.title()}'
        else:
            return f'{self.first_name.title()} {self.last_name.title()}'

class MembershipType(models.Model):
    name = models.CharField(max_length=200)
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    updated_date = models.DateField(auto_now=True)
    created_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-created_date']


    def __str__(self):
        return self.name

class Membership(models.Model):
    name = models.CharField(max_length=200)
    number = models.BigIntegerField()
    type_id = models.ForeignKey(MembershipType,on_delete=models.CASCADE)
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    updated_date = models.DateField(auto_now=True)
    created_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.name

class MembershipFeedback(models.Model):
    member_id = models.ForeignKey(Membership,on_delete=models.CASCADE)
    feedback = models.TextField()
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    updated_date = models.DateField(auto_now=True)
    created_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-created_date']



    def __str__(self):
        return self.member_id.number

