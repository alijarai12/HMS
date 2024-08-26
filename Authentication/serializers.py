from rest_framework import serializers
from .models import (
    Hotel, User, ResetPasswordOtp
)
from Employee.serializers import *

class UserProfileSerializer(serializers.ModelSerializer):
    employeeinfos = GetEmployeeInfoSerializer()
    class Meta:
        model = User
        fields = ['id','employeeinfos']

class AdminUserSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True)
    class Meta:
        model = Hotel
        fields = ['id','hotel_name','users']


class HotelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hotel
        fields = '__all__'
        


class SuperUserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)

    class Meta:
        model = User
        fields = ("id", "username", "password", "email")

    def create(self, validated_data):
        user = User.objects.create_superuser(
            username=validated_data['username'],
            email=validated_data.get('email'),
        )
        user.set_password(validated_data['password'])  # Set the password
        user.save()  # Save the user with the hashed password
        return user


class StaffUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    hotel_id = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = User
        exclude = ("first_name", "last_name")
        
    def create(self, validated_data):
       
        user = User.objects.create_staffuser(
            username=validated_data['username'],
            password=validated_data.get['password'],
            email=validated_data.get('email',),
            hotel_id=validated_data.get('hotel_id')
        )
        return user
    
    
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id','name']


#
class ResetPasswordOtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResetPasswordOtp
        fields = '__all__'


class ResetPasswordRequestSerializer(serializers.Serializer):
    mobile_number = serializers.IntegerField()

class ResetPasswordVerifySerializer(serializers.Serializer):
    otp = serializers.CharField()
    password = serializers.CharField()

