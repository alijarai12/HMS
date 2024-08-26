from django.urls import path
from .views import *

from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('organizationtype/',OrganizationTypeList.as_view(),name='organizationtypes'),
    path('organizationtype/<int:pk>/',OrganizationTypeDetail.as_view(),name='organizationtypedetail'),

    path('organization/',OrganizationList.as_view(),name='organizations'),
    path('organization/<int:pk>/',OrganizationDetail.as_view(),name='organizationdetail'),

    path('guesttype/',GuestTypeList.as_view(),name='guesttypes'),
    path('guesttype/<int:pk>/',GuestTypeDetail.as_view(),name='guesttypedetail'),

    path('guest/',GuestList.as_view(),name='guests'),
    path('guest/<int:pk>/',GuestDetail.as_view(),name='guestdetail'),

    path('membership/',MembershipList.as_view(),name='membership'),
    path('membership/<int:pk>/',MembershipDetail.as_view(),name='membershipdetail'),
    
    path('membershiptype/',MembershipTypeList.as_view(),name='membershiptype'),
    path('membershiptype/<int:pk>/',MembershipTypeDetail.as_view(),name='membershiptypedetail'),
    
    path('membershipfeedback/',MembershipFeedbackList.as_view(),name='membershipfeedback'),
    path('membershipfeedback/<int:pk>/',MembershipFeedbackDetail.as_view(),name='membershipfeedback'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
