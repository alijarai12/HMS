from rest_framework import serializers
from .models import RoomType, Room, BookingType, Booking, Service, RoomService, CheckIn, PackageType, Package
from Employee.serializers import *

class GetRoomTypeSerializer(serializers.ModelSerializer):
    hotel_id=HotelSerializer()
    class Meta:
        model = RoomType
        fields = '__all__'

class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = '__all__'


class GetRoomSerializer(serializers.ModelSerializer):
    room_type_id = RoomTypeSerializer()  # Serialize the RoomType model within RoomSerializer
    hotel_id = HotelSerializer()

    class Meta:
        model = Room
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class GetBookingTypeSerializer(serializers.ModelSerializer):
    hotel_id = HotelSerializer()
    class Meta:
        model = BookingType
        fields = '__all__'

class BookingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingType
        fields = '__all__'

class GetBookingSerializer(serializers.ModelSerializer):
    hotel_id = HotelSerializer()
    booking_type = BookingTypeSerializer()  # Serialize the BookingType model within BookingSerializer
    room = RoomSerializer()  # Serialize the Room model within BookingSerializer

    class Meta:
        model = Booking
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = '__all__'

class GetServiceSerializer(serializers.ModelSerializer):
    hotel_id = HotelSerializer()
    class Meta:
        model = Service
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class GetRoomServiceSerializer(serializers.ModelSerializer):
    service = ServiceSerializer() 
    room = RoomSerializer()  
    hotel_id = HotelSerializer
    class Meta:
        model = RoomService
        fields = '__all__'

class RoomServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = RoomService
        fields = '__all__'


class GetCheckInSerializer(serializers.ModelSerializer):
    room = RoomSerializer()  # Serialize the Room model within CheckInSerializer
    hotel_id = HotelSerializer
    class Meta:
        model = CheckIn
        fields = '__all__'

class CheckInSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = CheckIn
        fields = '__all__'


class GetPackageTypeSerializer(serializers.ModelSerializer):
    hotel_id = HotelSerializer
    class Meta:
        model = PackageType
        fields = '__all__'

class PackageTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageType
        fields = '__all__'

class GetPackageSerializer(serializers.ModelSerializer):
    package_type = PackageTypeSerializer()  # Serialize the PackageType model within PackageSerializer
    hotel_id = HotelSerializer
    class Meta:
        model = Package
        fields = '__all__'

class PackageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Package
        fields = '__all__'
