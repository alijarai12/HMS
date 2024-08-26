from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(RoomType)
admin.site.register(Room)
admin.site.register(BookingType)
admin.site.register(Booking)
admin.site.register(Service)
admin.site.register(RoomService)
admin.site.register(PackageType)
admin.site.register(Package)
admin.site.register(CheckIn)
