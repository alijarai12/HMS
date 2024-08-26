from django.db import models
from Guest.models import Guest
from datetime import datetime
from Authentication.models import Hotel

# Create your models here.
class RoomType(models.Model):
    name = models.CharField(max_length=50)
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    

    def __str__(self):
        return self.name


class Room(models.Model):
    STATUS_CHOICES = (
        ('Vacant', 'Vacant'),
        ('Occupied', 'Occupied'),
        ('Cleaning', 'Cleaning'),
    )

    name = models.CharField(max_length=50)
    room_no = models.IntegerField()
    room_type_id = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    description = models.TextField()
    floor_no = models.IntegerField()
    capacity = models.IntegerField()
    bed_count = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.name} - Room {self.room_no}"


class BookingType(models.Model):
    name = models.CharField(max_length=50)
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.name



class Booking(models.Model):
    STATUS_CHOICES = (
        ('booked', 'Booked'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
        ('cancelled', 'Cancelled'),
    )

    name = models.CharField(max_length=100)
    number = models.IntegerField()
    email = models.EmailField()
    extra_info = models.TextField(blank=True, null=True)
    booking_type = models.ForeignKey(BookingType, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='booked')
    cancelled_reason = models.TextField(blank=True, null=True)
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    def __str__(self):
        return f"Booking for {self.name} - Room {self.room.room_no}"
    

class Service(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )

    service_name = models.CharField(max_length=100)
    service_description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.service_name
    

class RoomService(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.service.service_name} - Room {self.room.room_no}"
    
class CheckIn(models.Model):
    guest_id = models.ForeignKey(Guest, on_delete=models.CASCADE)
    room_id =models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in_time = models.DateTimeField(default=datetime.now)
    check_out_time = models.DateTimeField(blank=True, null=True)
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    def __str__(self):
        return f"Check-in for {self.guest_id.first_name} in Room {self.room_id.room_no}"
    
class PackageType(models.Model):
    name = models.CharField(max_length=100)
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)


    def __str__(self):
        return self.name 
    
class Package(models.Model):

    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )

    name = models.CharField(max_length=100)
    description = models.TextField()
    package_type = models.ForeignKey(PackageType, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    end_time = models.TimeField(null=True, blank=True)
    total_price = models.IntegerField()
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.name