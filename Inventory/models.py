from django.db import models
from Authentication.models import Hotel
from Employee.models import *
# Create your models here.


class SupplierType(models.Model):
    type = models.CharField(max_length=255)
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE,related_name='suppliertypes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.type)

class Supplier(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    type = models.ForeignKey(SupplierType, on_delete=models.CASCADE,related_name='suppliers')
    contact_no = models.CharField(max_length=900)
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE,related_name='suppliers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.name)


class ProductCategory(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField()
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE,related_name='productcategories')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return str(self.name)


class Product(models.Model):
    stock_item_status_list = [('Available','Available'),('Unavailable','Unavailable')]

    status = models.CharField(max_length=50,choices=stock_item_status_list)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE,related_name='products')
    brand = models.CharField(max_length=255)
    detail_desc = models.TextField()
    image = models.ImageField(upload_to='media/product_image/',null=True)
    product_name=models.CharField(max_length=300)
    product_unit=models.CharField(max_length=300,null=True)
    quantity=models.BigIntegerField()
    department=models.ForeignKey(Department,on_delete=models.CASCADE,related_name='stockitems',null=True)
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE,related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.product_name)

# class StockList(models.Model):
#     department=models.ForeignKey(Department,on_delete=models.CASCADE,related_name='stocklists')
#     hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE,related_name='stocklists')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return str(self.department)

# 

class PurchaseOrderList(models.Model):
    STATUS_CHOICES = [
    ('In Progress', 'In Progress'),
    ('Completed', 'Completed'),
    # ...
]
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE,related_name='purchaseorderlists')
    discount_perc = models.FloatField(null=True)
    discount = models.FloatField(null=True)
    remark = models.TextField(null=True)
    tax_perc = models.FloatField(null=True)
    tax = models.FloatField(null=True)
    status = models.CharField(choices=STATUS_CHOICES,null=True, max_length=255)
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total=models.FloatField(null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.supplier)
    
    
    


class PurchaseOrderItems(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='purchaseorderitems')
    purchase_order_list=models.ForeignKey(PurchaseOrderList,on_delete=models.CASCADE,related_name='purchaseorderitems',null=True)
    quantity = models.BigIntegerField()
    unit_price = models.BigIntegerField()
    subtotal = models.FloatField()
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE,related_name='purchaseorderitems')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.product)
    
    def save(self,*args, **kwargs):
        prev_quantity = self.product.quantity
        self.product.quantity = self.quantity + prev_quantity
        self.product.save()
        super(PurchaseOrderItems,self).save(*args,**kwargs)



class StoreRequest(models.Model):
    STATUS_CHOICES = [
    ('New','New'),
    ('Denied', 'Denied'),
    ('Granted', 'Granted'),
]
    requesting_department = models.ForeignKey(Department, on_delete=models.CASCADE,related_name='storerequests')
    products = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='storerequests')
    quantity = models.BigIntegerField()
    desired_delivery_date = models.DateField()
    status = models.CharField(choices=STATUS_CHOICES, max_length=255, default='New')
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE,related_name='storerequests')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.requesting_department)

class ReturnProductDetails(models.Model):
    purchase_order_item = models.ForeignKey(PurchaseOrderItems, on_delete=models.CASCADE,related_name='returnproductdetails')
    return_date = models.DateField()
    reason = models.TextField()
    return_quantity = models.BigIntegerField()
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE,related_name='returnproductdetails')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.purchase_order_item)
    
    def save(self,*args, **kwargs):
        prev_quantity = self.purchase_order_item.product.quantity
        self.purchase_order_item.product.quantity = prev_quantity - self.return_quantity
        self.purchase_order_item.product.save()
        super(ReturnProductDetails,self).save(*args,**kwargs)

# class ProductReceivedDetails(models.Model):
#     purchase_order_items = models.ForeignKey(PurchaseOrderItems, on_delete=models.CASCADE,related_name='ProductsReceived')
#     remarks = models.TextField()
#     quantity = models.IntegerField()
#     hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE,related_name='ProductsReceived')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)


#     def __str__(self):
#         return str(self.purchase_order_items)

