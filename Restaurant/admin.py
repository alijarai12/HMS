from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Table)
admin.site.register(TableReservation)
admin.site.register(Menu)
admin.site.register(Food)
admin.site.register(OrderItem)
admin.site.register(RestaurantInvoice)
admin.site.register(RestaurantTransaction)
# admin.site.register(VAT)
# admin.site.register(ServiceCharge)
# admin.site.register(Discount)
admin.site.register(TaxAndDiscount)
admin.site.register(Offer)
admin.site.register(Banners)
admin.site.register(Contact)
admin.site.register(OpeningHours)
admin.site.register(Review)
admin.site.register(Subscriptions)
admin.site.register(Gallary)
admin.site.register(Floor)
admin.site.register(TotalCredit)
