from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
  path('dashboarddata/<int:pk>/',DashboardApiListView.as_view(),name='dashboarddatalist'),

  path('tables/',TableList.as_view(),name='tablelist'),
  path('tables/<int:pk>/',TableDetail.as_view(),name='tabledetail'),
  
  path('tablereservations/',TableReservationList.as_view(),name='tablelist'),
  path('tablereservations/<int:pk>/',TableReservationDetail.as_view(),name='tablereservationdetail'),
 
  path('menulist/',MenuList.as_view(),name='menulist'),
  path('menulist/<int:pk>/',MenuDetail.as_view(),name='menudetail'),
 
  path('foods/',FoodList.as_view(),name='foods'),
  path('foods/<int:pk>/',FoodDetail.as_view(),name='fooddetail'),


  path('tableorders/<int:pk>/', TableOrdersListView.as_view(), name='table-orders-list'),
  path('vatdiscount/', GetVatAndDiscount.as_view(), name='vatdiscount'),
  path('vatdiscount/<int:pk>/', GetVatAndDiscountDetail.as_view(), name='vatdiscountdetail'),

  
  path('orderitem/',OrderItemList.as_view(),name='orderitems'),
  path('orderitem/<int:pk>/',OrderItemDetail.as_view(),name='orderitemdetail'),

  path('restaurantinvoice/',RestaurantInvoiceList.as_view(),name='restaurantinvoicelist'),
  path('restaurantinvoice/<int:pk>/',RestraurantInvoiceDetail.as_view(),name='restaurantinvoicedetail'),
  
  path('restauranttransaction/',RestaurantTransactionList.as_view(),name='restauranttransactionlist'),
  path('restauranttransaction/<int:pk>/',RestraurantTransactionDetail.as_view(),name='restauranttransactiondetail'),

  path('ilivemenu/<int:hotel_id>/', AnonymousMenuAPIView.as_view(), name='AnonymousMenuAPIView'),

  path('ilivefood/<int:hotel_id>/', AnonymousFoodAPIView.as_view(), name='AnonymousFoodAPIView'),

  path('ilivetable/<int:hotel_id>/', AnonymousTableAPIView.as_view(), name='AnonymousTableAPIView'),

  path('ilivereservedtable/<int:hotel_id>/', AnonymousTableReservationAPIView.as_view(), name='AnonymousTableReservationAPIView'),

  path('ilivebanner/', AnonymousBannerView.as_view(), name='AnonymousBannerview'),

  path('ilivecontact/', AnonymousContactView.as_view(), name='AnonymousBannerview'),

  path('iliveoffer/', AnonymousOfferview.as_view(), name='AnonymousOfferview'),

  path('iliveopeninghours/', OpeningHoursView.as_view(), name='OpeningHoursView'),

  path('ilivesubscriptions/', AnonymousSubscriptionView.as_view(), name='AnonymousSubscriptionView'),

  path('ilivegallery/', AnonymousGalleryView.as_view(), name='AnonymousGalleryView'),

  path('ilivemembership/', IliveMembershipApiView.as_view(), name='Membership'),

  path('floor/', FloorApiView.as_view(), name="FloorApiView"),
  path('floor/<int:pk>/', FloorApiView.as_view(), name="FloorApiView"),

  path('total-credit/', TotalCreditView.as_view(), name="TotalCreditView"),

  path('credit-detail/', CreditDetailsView.as_view(),name="CreditDetailsView"),
  
  path('ilivecontactinfo/', IliveContactInfoView.as_view(), name="contatinformation"),
  
  path('ilivecontactinfo/<int:pk>/', IliveContactInfoView.as_view(), name="contatinformation"),
 


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)