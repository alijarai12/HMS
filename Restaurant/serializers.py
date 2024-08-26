from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.db.models import Sum
from datetime import datetime, timedelta
from django.db.models import Count

from .models import *
from Employee.serializers import *
from Guest.serializers import *
from Payment.serializers import PaymentMethodSerializer, BankInfoSerializer
from Expenses.models import *
from Expenses.serializers import *
from Inventory.models import *
from Inventory.serializers import *
import json

class GetTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        exclude = ['latest_table_token']

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        exclude = ['latest_table_token']

class GetTableReservationSerializer(serializers.ModelSerializer):
    hotel_id=HotelSerializer()
    table=TableSerializer()
    guest = GuestSerializer()

    class Meta:
        model = TableReservation
        fields = '__all__'
        # exclude = ['hotel_id']


class TableReservationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TableReservation
        fields = '__all__'
        

        

class GetMenuSerializer(serializers.ModelSerializer):
    # hotel_id=HotelSerializer()

    class Meta:
        model = Menu
        # fields = '__all__'
        exclude = ['hotel_id']

class MenuSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Menu
        fields = '__all__'


class GetFoodSerializer(serializers.ModelSerializer):
    # hotel_id=HotelSerializer()
    menu=MenuSerializer()

    class Meta:
        model = Food
        # fields = '__all__'
        exclude = ['hotel_id']



class FoodSerializer(serializers.ModelSerializer):

    class Meta:
        model = Food
        fields = '__all__'

class GetOrderItemSerializer(serializers.ModelSerializer):
    food = GetFoodSerializer()
    table_id = GetTableSerializer()
    order_placed_by = EmployeeInfoSerializer()


    class Meta:
        model = OrderItem
        exclude = ['latest_table_token', 'hotel_id']
    

class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        exclude = ['latest_table_token']
        

class GetRestaurantInvoiceSerializer(serializers.ModelSerializer):
    order = GetOrderItemSerializer()
    
    class Meta:
        model = RestaurantInvoice
        exclude = ['hotel_id']
        extra_kwargs = {'restaurant_transaction':{'write_only':True}}

class RestaurantInvoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = RestaurantInvoice
        fields = '__all__'

class RestaurantInvoiceGuestSerializer(serializers.ModelSerializer):

    class Meta:
        model = RestaurantInvoice
        fields = '__all__'

    def validate_related_field(self, value):
        if value is None:
            raise serializers.ValidationError("This field is required.")
        return value

class GetRestaurantTransactionSerializer(serializers.ModelSerializer):
    confirmed_by = EmployeeInfoSerializer()
    # order = OrderSerializer()
    restaurant_invoice = GetRestaurantInvoiceSerializer(many=True)
    payment_method = PaymentMethodSerializer()
    bank_details = BankInfoSerializer()
    # hotel_id=HotelSerializer()

    class Meta:
        model = RestaurantTransaction
        #fields = '__all__'
        exclude = ['hotel_id']
        read_only_fields = ['bill_number']

class RestaurantTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantTransaction
        fields = '__all__'
        #exclude = ['bill_number']  # Exclude bill_number from POST/PUT requests
        read_only_fields = ['bill_number']




class GetVatAndDiscountSerializer(serializers.ModelSerializer):
    # hotel_id = HotelSerializer()
    class Meta:
        model = TaxAndDiscount
        # fields = '__all__'
        exclude = ['hotel_id']


class VatAndDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxAndDiscount
        fields = '__all__'
    

class GetTableOrdersListSerializers(serializers.ModelSerializer):
    table_id = TableSerializer()
    food = FoodSerializer()
    vat_discount = GetVatAndDiscountSerializer(source='hotel_id.vat_sc_discount', read_only=True)
    class Meta:
        model = OrderItem
        exclude = ['updated_date','created_date','hotel_id']


class DashboardDataSerializer():
    def get_data(self,hotel_id,year=datetime.now().year):
        # Filter data for a specific day
        current_date = datetime.now()
        # start_of_week = current_date - timedelta(days=current_date.weekday())
        current_week_number = current_date.isocalendar()[1]

        # print(start_of_week)
        week_revenue = {}
        month_revenue = {}
        week_expense = {}
        month_expense = {}


        total_day_revenue = RestaurantTransaction.objects.filter(hotel_id=hotel_id,created_at__date=current_date).aggregate(total_day_revenue = Sum('total'))['total_day_revenue']
        total_day_expense = Expense.objects.filter(hotel_id=hotel_id,created_at__date=current_date).aggregate(total_day_expense = Sum('amount'))['total_day_expense']

        if total_day_revenue is None:
            total_day_revenue = 0
        if total_day_expense is None:
            total_day_expense = 0 

        for i in range(1,8):
            total_week_revenue = RestaurantTransaction.objects.filter(hotel_id=hotel_id,created_at__year=year,created_at__week=current_week_number,created_at__week_day=i).aggregate(total_week_revenue = Sum('total'))['total_week_revenue']
            total_week_expense = Expense.objects.filter(hotel_id=hotel_id,created_at__year=year,created_at__week=current_week_number,created_at__week_day=i).aggregate(total_week_expense = Sum('amount'))['total_week_expense']

            if total_week_revenue is None:
                total_week_revenue = 0
            if total_week_expense is None:
                total_week_expense = 0
            week_revenue[i] = total_week_revenue  
            week_expense[i] = total_week_expense  

        for i in range(1,13):
            total_month_revenue = RestaurantTransaction.objects.filter(hotel_id=hotel_id,created_at__year=year,created_at__month=i).aggregate(total_month_revenue = Sum('total'))['total_month_revenue']
            total_month_expense = Expense.objects.filter(hotel_id=hotel_id,created_at__year=year,created_at__month=i).aggregate(total_month_expense = Sum('amount'))['total_month_expense']
            if total_month_revenue is None:
                total_month_revenue = 0
            if total_month_expense is None:
                total_month_expense = 0

            month_revenue[i] = total_month_revenue  
            month_expense[i] = total_month_expense    

        total_year_revenue = RestaurantTransaction.objects.filter(hotel_id=hotel_id,created_at__year=year).aggregate(total_year_revenue = Sum('total'))['total_year_revenue']  
        total_year_expense = Expense.objects.filter(hotel_id=hotel_id,created_at__year=year).aggregate(total_year_expense = Sum('amount'))['total_year_expense']  

        if total_year_revenue is None:
            total_year_revenue = 0
        if total_year_expense is None:
            total_year_expense= 0

        total_year_profit = total_year_revenue - total_year_expense

        out_of_stock_range = range(0,5)

        product_count = Product.objects.filter(hotel_id=hotel_id,status='Available',created_at__year=year).count()

        low_stock_product = Product.objects.filter(hotel_id=hotel_id,status='Available', quantity__in=out_of_stock_range,created_at__year=year).count()



        guest_count = Guest.objects.filter(hotel_id=hotel_id,is_available = True,created_date__year=year).count()

        member_count = Membership.objects.filter(hotel_id=hotel_id,created_date__year=year).count()

        return {
            'day_revenue' : total_day_revenue,
            'week_revenue' : week_revenue,
            'month_revenue' : month_revenue,
            'year_revenue' : total_year_revenue,
            'day_expense' : total_day_expense,
            'week_expense' : week_expense,
            'month_expense' : month_expense,
            'year_expense' : total_year_expense,
            'total_year_profit' : total_year_profit,
            'product_count' : product_count,
            'guest_count' : guest_count,
            'member_count' : member_count,
            'low_stock_product' : low_stock_product

        }



class BannersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banners
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class GetOfferSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Offer
        fields = '__all__'



class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'


class OpeningHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpeningHours
        fields = '__all__'

class GallarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallary
        fields = '__all__'

class SubscriptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriptions
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class FloorSerializer(serializers.ModelSerializer):  

    class Meta:
        model = Floor
        fields = '__all__'

class GetFloorSerilizer(serializers.ModelSerializer):
    hotel_id = HotelSerializer()
    tables = TableSerializer(many=True) 
    class Meta:
        model = Floor
        fields = ['id', 'tables', 'name', 'hotel_id']

class TotalCreditSerilizer(serializers.ModelSerializer):

    class Meta:
        model = TotalCredit
        fields = '__all__'


class CreditDetailsSerillizers(serializers.ModelSerializer):
    total = TotalCreditSerilizer
    class Meta:
        model = CreditDetails
        fields = '__all__'
        
class GetCreditDetailsSerillizers(serializers.ModelSerializer):
    hotel = HotelSerializer
    class Meta:
        model = CreditDetails
        fields = '__all__'
        
class GetInformationSerillizers(serializers.ModelSerializer):

    class Meta:
        model = Hotel 
        fields = '__all__'

