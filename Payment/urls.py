from django.urls import path, include
from .views import *

urlpatterns = [
    
path('paymentmethod/',PaymentMethodList.as_view(),name='paymentmethods'),
path('paymentmethod/<int:pk>/',PaymentMethodDetail.as_view(),name='paymentmethoddetail'),
path('bankinfo/',BankInfoList.as_view(),name='bankinfos'),
path('bankinfo/<int:pk>/',BankInfoDetail.as_view(),name='bankinfo'),



]