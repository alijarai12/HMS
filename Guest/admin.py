from django.contrib import admin
from .models import *

admin.site.register(OrganizationType)
admin.site.register(Organization)
admin.site.register(GuestType)
admin.site.register(Guest)
admin.site.register(MembershipType)
admin.site.register(Membership)
admin.site.register(MembershipFeedback)