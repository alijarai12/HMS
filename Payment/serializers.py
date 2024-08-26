from rest_framework import serializers
from .models import PaymentMethod, BankInfo
from Authentication.serializers import *
from Employee.serializers import *
from Restaurant.serializers import *


class GetPaymentMethodSerializer(serializers.ModelSerializer):
    # hotel_id = HotelSerializer()
    class Meta:
        model = PaymentMethod
        # fields = '__all__'
        exclude = ['hotel_id']

class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'

class GetBankInfoSerializer(serializers.ModelSerializer):
    # hotel_id = HotelSerializer()

    class Meta:
        model = BankInfo
        # fields = '__all__'
        exclude = ['hotel_id']

class BankInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = BankInfo
        fields = '__all__'

    
