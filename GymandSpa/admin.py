from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Gym),
admin.site.register(GymPackages),
admin.site.register(GymAttendance),
admin.site.register(GymFeedback),
admin.site.register(NutritionPlan),
admin.site.register(GymMember),
admin.site.register(GymInvoice),

admin.site.register(Spa),
admin.site.register(SpaBooking),
admin.site.register(SpaFeedback),
admin.site.register(SpaPackage),
admin.site.register(SpaService),
admin.site.register(SpaInvoice),
admin.site.register(SpaMember),