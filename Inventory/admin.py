from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(SupplierType)
admin.site.register(Supplier)
admin.site.register(ProductCategory)
admin.site.register(Product)
# admin.site.register(StockItem)

admin.site.register(PurchaseOrderList)
admin.site.register(PurchaseOrderItems)
admin.site.register(StoreRequest)
admin.site.register(ReturnProductDetails)
