from rest_framework import serializers
from .models import *
from Employee.serializers import *


class GetExpenseSerializer(serializers.ModelSerializer):
    # hotel_id = HotelSerializer()
    department = DepartmentSerializer()
    class Meta:
        model = Expense
        # fields = '__all__'
        exclude = ['hotel_id']


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'


class GetExpenseStatusSerializer(serializers.ModelSerializer):
    expense = ExpenseSerializer()
    # hotel_id = HotelSerializer()
    accepted_by = EmployeeInfoSerializer()

    class Meta:
        model = ExpenseStatus
        # fields = '__all__'
        exclude = ['hotel_id']


class ExpenseStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseStatus
        fields = '__all__'