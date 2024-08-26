from django.urls import path
from .views import *

urlpatterns = [
    path('roomtype/',RoomTypeApi.as_view(), name='Roomtype'),
    path('roomtype/',RoomTypeApi.as_view(), name='Roomtype'),

    path('room/',RoomApi.as_view(), name='Room'),
    path('room/<int:pk>/',RoomApi.as_view(), name='Room'),

    path('booking/',BookingApi.as_view(), name='Booking'),
    path('booking/<int:pk>/',BookingApi.as_view(), name='Booking'),

    path('bookingtype/',BookingTypeApi.as_view(), name='BookingType'),

    path('service/',ServiceApi.as_view(), name='service'),
    path('service/<int:pk>/',ServiceApi.as_view(), name='service'),

    path('roomservice/', RoomServiceApi.as_view(), name='RoomService'),
    path('roomservice/<int:pk>/', RoomServiceApi.as_view(), name= 'RoomServiceApi'),

    path('checkin/', CheckInApi.as_view(), name='CheckInApi'),
    path('checkin/<int:pk>/', CheckInApi.as_view(), name='CheckInApi'),

    path('package/', PackageApi.as_view(), name='Package'),
    path('package/<int:pk>/', PackageApi.as_view(), name='Package'),
    
    path('packagetype/', PackageTypeApi.as_view(), name='Packagetype'),
    path('packagetype/<int:pk>/', PackageTypeApi.as_view(), name='Packagetype')

    
]
