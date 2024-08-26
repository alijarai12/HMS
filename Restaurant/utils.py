from datetime import datetime, timedelta
from .models import *
from rest_framework import permissions


def check_table_availability(request_data):
    """
    Check if the table's free to book around the given time. 
    We're looking 2 hours before and after the specified time.
    """
    table_id = request_data.get('table')
    booking_time_str = request_data.get('bookingDateTime')
    
    # Convert the string to a datetime object for further processing
    booking_time = datetime.strptime(booking_time_str, "%Y-%m-%dT%H:%M:%S%z")

    # Calculate the start and end times for the overlap window
    overlap_start_time = booking_time - timedelta(hours=2)
    overlap_end_time = booking_time + timedelta(hours=2)

    # Check if a reservation already exists for the table within the overlap window
    exists = TableReservation.objects.filter(table=table_id, 
                                             bookingDateTime__gte=overlap_start_time, 
                                             bookingDateTime__lte=overlap_end_time).exists()
    return exists




#filter querysets by logged in user's hotel_id
class HotelIDFilterMixin:
    """
        Mixin to filter querysets by hotel_id.
        - If the user is a superuser, all objects are returned.
        - If the user is an authenticated non-superuser, only objects associated with their hotel_id are returned.
        - For unauthenticated users, an empty queryset is returned.
    """
    def filter_by_hotel(self, queryset):
        if self.request.user.is_superuser:
            return queryset.all()
        elif self.request.user.is_authenticated:
            print(self.request.user.hotel_id)
            return queryset.filter(table__hotel_id=self.request.user.hotel_id)
        return queryset.none()  # Return an empty queryset for unauthenticated users
    


class HotelAssociatedObjj(permissions.BasePermission):
    """
    Permission check to ensure:
        1. The user is authenticated.
        2. Superusers are granted permission.
        3. Authenticated non-superusers can only access objects associated with their hotel.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        if not hasattr(view, 'queryset_model'):
            return False
        obj_id = view.kwargs.get('pk')
        if not obj_id:
            return False

        try:
            obj = view.queryset_model.objects.get(pk=obj_id)
            obj_hotel_id = obj.table.hotel_id
            return obj_hotel_id == request.user.hotel_id
        except view.queryset_model.DoesNotExist:
            return False