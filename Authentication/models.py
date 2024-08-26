from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import *

# Create your models here.
class Hotel(models.Model):
    hotel_name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='hotel_image', blank=True, null=True)
    ceo = models.CharField(max_length=300)
    contact = models.CharField(max_length=300)
    contact_2 = models.CharField(max_length=300, null=True, blank=True)
    email = models.EmailField(unique=True)
    website = models.URLField(null=True, blank=True)
    address = models.CharField(max_length=300)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)    
    twitter_url = models.URLField(null=True, blank=True)
    facebook_url = models.URLField(null=True, blank=True)
    instagram_url = models.URLField(null=True, blank=True)
    youtube_url = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ['-created_date']
     
    def __str__(self):
        return self.hotel_name
    


# Create your models here.
class User(AbstractUser):
    username = models.CharField(null=True,max_length=300,blank=True,default='default_username')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=300)
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='users', blank= True, null=True)    
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    phone_number = models.CharField(max_length=15, default='', blank=True)



    USERNAME_FIELD='email'
    REQUIRED_FIELDS = ['username','phone_number']

    def __str__(self):
        return self.email

    objects = UserManager()


class ResetPasswordOtp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OTP: {self.otp} for User: {self.user.username}"


    

