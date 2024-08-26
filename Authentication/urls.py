from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [

    path('hotel/', HotelList.as_view()),

    path('hotel/<int:pk>/', HotelDetail.as_view()),

    path('user/', UserList.as_view()),

    path('user/<int:pk>/', UserDetail.as_view()),

    
    path('superuser/<int:pk>/', SuperUserRegisterAPIIdView.as_view(), name='superuser-id'),

    path('register/superuser/', SuperUserRegistrationView.as_view(), name='superuser-register'),

    path('creategroups/', CreateGroupsAndPermissionsView.as_view(), name='create_groups_permissions'),

    path('createadmin/',AdminUserView.as_view(),name='create-admin'),

    path('role/',GroupAPIView.as_view(),name='role'),

    
    path('login/', UserLoginApiView.as_view(), name='login'),
    
    path('logout/', UserLogoutApiView.as_view(), name='logout'),

    #
    path('resetpassword/', views.reset_password_otp, name='reset_password_otp'),
    path('verifyotp/', views.reset_password_otp_verify, name='reset_password_otp_verify'),
    path('changepassword/', views.change_password, name='change_password'),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
