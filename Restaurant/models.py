from typing import Iterable, Optional
from django.db import models
from Employee.models import *
from Guest.models import *
from Payment.models import*
import random
from django.urls import reverse
from datetime import datetime

# Create your models here.

class Floor(models.Model):
    name = models.CharField(max_length=50)
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='floors')

    def __str__(self):
        return str(self.name)
    
    class Meta:
        unique_together = ['hotel_id', 'name']
        ordering = ['id']


class Table(models.Model):
    table_no = models.IntegerField()
    seating_capacity = models.IntegerField()
    is_occupied = models.BooleanField(default=False)
    latest_table_token = models.CharField(max_length=10,null=True)
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='tables')
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name='tables', null=True)

    def __str__(self):
        return str(self.table_no)

    def save(self,*args, **kwargs):
        if self.is_occupied == True and not self.latest_table_token:
            # random_token_number = random.randint(10000, 99999)
            self.latest_table_token = str(random.randint(10000,99999))
        elif not self.is_occupied:
            self.latest_table_token = None
        super(Table,self).save(*args,**kwargs)

    class Meta:
        unique_together = ['table_no','hotel_id', 'floor']
        ordering = ['table_no']


class TableReservation(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE,null=True,blank=True ,related_name='tablereservations')
    name=models.CharField(max_length=300,null=True,blank=True)
    contact=models.BigIntegerField(null=True,blank=True)
    isGuest=models.BooleanField(default=False,null=True)
    table = models.ForeignKey(Table, on_delete=models.CASCADE,default=1, related_name='tablereservations')
    bookingDateTime = models.DateTimeField(null=True)
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='tablereservations')
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    
    def __str__(self):
        return (str(self.name))
    
    class Meta:
        ordering = ['-created_date']
        unique_together = ('table', 'bookingDateTime')



class Menu(models.Model):
    menuType = models.CharField(max_length=300)
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='menus')
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.menuType
    
    class Meta:
        ordering = ['-created_date']


class Food(models.Model):
    food_name = models.CharField(max_length=300)
    ingredients = models.TextField()
    unit = models.CharField(max_length=300)  
    unit_price = models.BigIntegerField()
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='foods')
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='foods')
    food_image = models.ImageField(upload_to='food_images/', null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.food_name
    
    class Meta:
        ordering = ['-created_date']



STATUS_CHOICES = [
        ('completed', 'completed'),
        ('pending', 'pending'),
        ('cancel', 'cancel')
    ]
        


class OrderItem(models.Model):
    status = (('In Progress', 'In Progress'),('Cancelled','Cancelled'),('Completed', 'Completed'))
    table_id = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='orderitems')
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='orderitems')
    quantity = models.BigIntegerField(default=0)
    notes = models.TextField(null=True, blank=True)
    latest_table_token = models.CharField(max_length=10,null=True)
    order_no = models.CharField(max_length=10)
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='orderitems')
    order_status= models.CharField(choices=status, default='In Progress', max_length=300)
    order_placed_by =models.ForeignKey(EmployeeInfo, on_delete= models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    
    def __str__(self):
        return (str(self.food.food_name))
    
    def save(self,*args, **kwargs):
        if not self.table_id.is_occupied:
            self.table_id.is_occupied=True
            self.table_id.save()
        # latest_table_token = self.table_id.latest_table_token
        self.latest_table_token = self.table_id.latest_table_token
        super(OrderItem,self).save(*args,**kwargs)

    class Meta:
        ordering = ['-created_date']



class RestaurantTransaction(models.Model): 
    confirmed_by = models.ForeignKey(EmployeeInfo, on_delete=models.CASCADE,null=True)
    guest_name = models.CharField(max_length=80,null=True)
    guest_number = models.BigIntegerField(null=True)
    vat = models.FloatField(default=0.00,null=True)
    service_fee = models.FloatField(default=0.00,null=True)
    discount = models.FloatField(default=0.00,null=True)
    discount_reason = models.TextField(null=True,blank=True)
    total = models.FloatField(default=0.00,null=True)
    received_amount = models.FloatField(default=0.00,null=True)
    change_returned =models.FloatField(default=0.00,null=True)  
    payment_method = models.ForeignKey(PaymentMethod,null=True,blank=True, on_delete=models.CASCADE)
    bank_details = models.ForeignKey(BankInfo,null=True,blank=True, on_delete=models.CASCADE)
    membership = models.ForeignKey(Membership,on_delete=models.CASCADE,null=True)
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    bill_number = models.CharField(max_length=20,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def generate_bill_number(self):
        now = datetime.now()
        random_part = str(random.randint(1000, 9999))  # Generate a 4-digit random number
        bill_number = f"{random_part}"
        return bill_number

    def save(self, *args, **kwargs):
        if not self.bill_number: # generating bill number for restaurant transaction
            self.bill_number = self.generate_bill_number()

        if self.payment_method != None and self.payment_method.name.lower() == "credit": # if payment method is not non and if payment method is credit then credit management

            if self.membership is None and self.guest is None: # If memebership is not none then it is for outside guests so the credit management is done for guest

                if isinstance(self.hotel_id, Hotel): # getting hotel instance to create total credit for the guest
                    hotel_instance = self.hotel_id
                else:
                    hotel_instance = Hotel.objects.get(id=self.hotel_id)

                try: # getting total credit if the guest already had total credit but if the guest doesnot have total credit , then creating one
                    t_c, created = TotalCredit.objects.get_or_create(guestnumber=self.guest_number, hotel_id=hotel_instance)

                except: # if total credit for the guest is many then filter it and get latest id total credit so that means the latest state of total credit for the guest number
                    t_c = TotalCredit.objects.filter(guestnumber=self.guest_number).latest('id')

                if t_c.credit_amount == 0: # If credit amount is 0 which is the case for creating a new total credit object for guest and also when total credit is reduced to 0 through payment, then the total is the credit amount
                    t_c.credit_amount = self.total
                    t_c.save()

                else: # If total credit amount is not 0 then add the total with prev credit amount and create a total credit object
                    total_credit = t_c.credit_amount + self.total
                    TotalCredit.objects.create(guestnumber=self.guest_number,credit_amount=total_credit, hotel_id=hotel_instance)

            elif self.membership != None: # Same as above credit management for guest, but below is for members 
                if isinstance(self.hotel_id, Hotel):
                    hotel_instance = self.hotel_id
                else:
                    hotel_instance = Hotel.objects.get(id=self.hotel_id)

                try:
                    t_c, created = TotalCredit.objects.get_or_create(membership=self.membership, hotel_id=hotel_instance)
                except:
                    t_c = TotalCredit.objects.filter(membership=self.membership,hotel_id=hotel_instance).latest('id')

                if t_c.credit_amount == 0:
                    t_c.credit_amount = self.total
                    t_c.save()
                else:

                    total_credit = t_c.credit_amount + self.total
                    TotalCredit.objects.create(membership=self.membership,credit_amount=total_credit, hotel_id=hotel_instance)
                    
        super(RestaurantTransaction, self).save(*args, **kwargs)

    def __str__(self):
        if self.membership != None:
            return self.membership.name
        return str(self.guest_name)
    
    class Meta:
        ordering = ['-created_at']
    

class RestaurantInvoice(models.Model):
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    order = models.ForeignKey(OrderItem,on_delete=models.SET_NULL,null=True)
    guest = models.ForeignKey(Guest,on_delete=models.CASCADE,null=True)
    for_guest = models.BooleanField(default=False)
    restaurant_transaction = models.ForeignKey('RestaurantTransaction',on_delete=models.CASCADE,related_name='restaurant_invoice',null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.guest)
    
    class Meta:
        ordering = ['-created_at']
    
    def save(self,*args, **kwargs):
        discount_perc = 0
        if self.restaurant_transaction != None: 
            discount_perc = self.restaurant_transaction.discount

        if discount_perc == 0.0:
            try:
                discount_perc = self.hotel_id.vat_sc_discount.discount
            except:
                pass
        try:
            service_charge_perc = self.hotel_id.vat_sc_discount.service_charge
        except:
            service_charge_perc = 0
        if self.for_guest != True:
            price = self.order.food.unit_price
            quantity = self.order.quantity
            total_amount = price * quantity
            discount_amount = total_amount * discount_perc / 100
            service_charge_amount = total_amount * service_charge_perc / 100
            total_before_vat = total_amount - discount_amount + service_charge_amount
            # vat_amount = total_before_vat * vat_perc / 100
            # total_after_vat = total_before_vat + vat_amount
            prev_total = self.restaurant_transaction.total
            if prev_total == None:
                new_total = total_before_vat
            else:
                new_total = prev_total + total_before_vat
            self.restaurant_transaction.total = new_total
            # self.restaurant_transaction.vat = vat_perc
            self.restaurant_transaction.discount = discount_perc
            self.restaurant_transaction.service_fee = service_charge_perc
            self.restaurant_transaction.save()

        super(RestaurantInvoice,self).save(*args,**kwargs)

class TotalCredit(models.Model):
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    restaurant_transaction = models.ForeignKey(RestaurantTransaction,on_delete=models.CASCADE,null=True)
    guestnumber = models.BigIntegerField(null=True)
    membership = models.ForeignKey(Membership, null=True, on_delete = models.SET_NULL)
    credit_amount = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

    class Meta:
        ordering = ['-id']

class CreditDetails(models.Model):
    credit_paid = models.FloatField()
    return_amount = models.FloatField(null=True)
    total_credit = models.ForeignKey(TotalCredit, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.total_credit:
            credit_amount = self.total_credit.credit_amount - self.credit_paid
            g_n = self.total_credit.guestnumber
            membership = self.total_credit.membership
            hotel = self.total_credit.hotel_id
            if g_n != None:
                total_credit = TotalCredit.objects.create(guestnumber=g_n,hotel_id=hotel,credit_amount=credit_amount )
            if membership != None:
                total_credit = TotalCredit.objects.create(membership=membership,hotel_id=hotel,credit_amount=credit_amount )
        super(CreditDetails, self).save(*args, **kwargs)

class TaxAndDiscount(models.Model):
    vat = models.FloatField(default=0,help_text="Rate in percentage")
    service_charge = models.FloatField(default=0,help_text="Rate in percentage")
    discount = models.FloatField(default=0,help_text="Rate in percentage")
    hotel_id = models.OneToOneField(Hotel, on_delete=models.CASCADE, related_name='vat_sc_discount')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.hotel_id.hotel_name
    
    class Meta:
        ordering = ['-created_at']


class VAT(models.Model):
    name = models.CharField(max_length=200)
    percentage = models.FloatField(default=0,help_text="Rate in percentage")
    hotel_id = models.OneToOneField(Hotel, on_delete=models.CASCADE, related_name='vat_rate')
    
    def __str__(self):
        return f"{self.name} - {self.percentage}%"



class ServiceCharge(models.Model):
    name = models.CharField(max_length=200)
    percentage = models.FloatField(default=0,help_text="Rate in percentage")
    hotel_id = models.OneToOneField(Hotel, on_delete=models.CASCADE, related_name='service_charge')

    def __str__(self):
        return f"{self.name} - {self.percentage}%"



class Discount(models.Model):
    name = models.CharField(max_length=200, help_text="Seasonal Discount")
    percentage = models.FloatField(default=0,help_text="Rate in percentage")
    hotel_id = models.OneToOneField(Hotel, on_delete=models.CASCADE, related_name='discount')

    def __str__(self):
        return f"{self.name} - {self.percentage}%"
    



class Banners(models.Model):
    banner_image = models.ImageField(upload_to='restaurant_banners/')
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    redirect_link = models.URLField()
    page_slug = models.SlugField(choices=[
        ('blog', 'Blog'),
        ('about-us', 'About Us'),
        ('contact', 'Contact'),
        ('home', 'Home'),
        ('menu','Menu')
        ])

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        # Define the URL where the "read more" link should redirect
        return reverse('page_detail', args=[str(self.page_slug)])
    
class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    title = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):

        return self.title
    
class Offer(models.Model):
    #menu_type = models.ForeignKey(Menu, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    day = models.CharField(max_length=255)
    time = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.menu_type} - {self.menu} ({self.day})"

class OpeningHours(models.Model):
    dayRange = models.CharField(max_length=255)
    time = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.dayRange} - {self.time}"


class Subscriptions(models.Model):
    email = models.EmailField()

class Gallary(models.Model):
    files =models.FileField()


class Review(models.Model):
    RATING_CHOICES = (
        (1, '1 - Very Poor'),
        (2, '2 - Poor'),
        (3, '3 - Average'),
        (4, '4 - Good'),
        (5, '5 - Excellent'),
    )

    rating = models.IntegerField(choices=RATING_CHOICES)
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"{self.rating} - {self.title}"


