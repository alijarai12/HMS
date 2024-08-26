from rest_framework import serializers
from .models import *
from django.contrib.auth.models import Group

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id','name']

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'
        

class GetUserSerializer(serializers.ModelSerializer):
    hotel_id=HotelSerializer()
    class Meta:
        model = User
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class GetEmployeePostSerializer(serializers.ModelSerializer):
    # hotel_id=HotelSerializer()

    class Meta:
        model = EmployeePost
        # fields = '__all__'
        exclude = ['hotel_id']


class EmployeePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmployeePost
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    manager_name = serializers.SerializerMethodField()


    def get_manager_name(self, instance):
        manager = instance.manager_name
        serializer = EmployeeInfoSerializer(manager)
        return serializer.data
    
    class Meta:
        model = Department
        fields = '__all__'


class GetEmployeeInfoSerializer(serializers.ModelSerializer):
    employee_role = GroupSerializer()
    user = UserSerializer()
    # hotel_id=HotelSerializer()
    department = DepartmentSerializer()
    post =EmployeePostSerializer()


    class Meta:
        model = EmployeeInfo
        # fields = '__all__'
        exclude = ['hotel_id']

class EmployeeInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmployeeInfo
        fields = '__all__'

class GetAttendanceDateSerializer(serializers.ModelSerializer):
    # hotel_id=HotelSerializer()

    class Meta:
        model = AttendanceDate
        # fields = '__all__'
        exclude = ['hotel_id']



class AttendanceDateSerializer(serializers.ModelSerializer):

    class Meta:
        model = AttendanceDate
        fields = '__all__'


class GetAttendanceSerializer(serializers.ModelSerializer):
    # hotel_id=HotelSerializer()
    employee=EmployeeInfoSerializer()
    attendance_date=AttendanceDateSerializer()

    class Meta:
        model = Attendance
        # fields = '__all__'
        exclude = ['hotel_id']


class AttendanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attendance
        fields = '__all__'

class GetShiftSerializer(serializers.ModelSerializer):
    # hotel_id=HotelSerializer()
    class Meta:
        model = Shift
        # fields = '__all__'
        exclude = ['hotel_id']


class ShiftSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shift
        fields = '__all__'




class GetEmployeeShiftSerializer(serializers.ModelSerializer):
    # hotel_id=HotelSerializer()
    employee = EmployeeInfoSerializer()
    shift_name = ShiftSerializer()

    class Meta:
        model = EmployeeShift
        # fields = '__all__'
        exclude = ['hotel_id']


class EmployeeShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeShift
        fields = '__all__'

        