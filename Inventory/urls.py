from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [

    path('suppliertype/', SupplierTypeList.as_view(),name='suppliertype'),
    path('suppliertype/<int:pk>/',SupplierTypeDetail.as_view(),name='suppliertypedetail'),
   
   
    path('supplier/',SupplierList.as_view(),name='supplier'),
    path('supplier/<int:pk>/',SupplierDetail.as_view(),name='supplierdetail'),


    path('productcategory/',ProductCategoryList.as_view(),name='productcategory'),
    path('productcategory/<int:pk>/',ProductCategoryDetail.as_view(),name='productcategorydetail'),


    path('product/',ProductList.as_view(),name='product'),
    path('product/<int:pk>/',ProductDetail.as_view(),name='productdetail'),



    # path('stockitem/',StockItemList.as_view(),name='stockitem'),
    # path('stockitem/<int:pk>/',StockItemDetail.as_view(),name='stockitemdetail'),
    

    path('purchaseorderlist/',PurchaseOrder.as_view(),name='purchaseorderlist'),
    path('purchaseorderlist/<int:pk>/',PurchaseOrderListDetail.as_view(),name='purchaseorderlistdetail'),


    path('purchaseorderitem/',PurchaseOrderItemsList.as_view(),name='purchaseorderitemlist'),
    path('purchaseorderitem/<int:pk>/',PurchaseOrderItemsDetail.as_view(),name='purchaseorderitemdetail'),


    path('storerequest/',StoreRequestList.as_view(),name='storerequestlist'),
    path('storerequest/<int:pk>/',StoreRequestDetail.as_view(),name='storerequestdetail'),

    path('returnproductdetail/',ReturnProductDetailsList.as_view(),name='returnproductlist'),
    path('returnproductdetail/<int:pk>/',ReturnProduct.as_view(),name='returnproductdetail'),

    path('productstockinfo/',ProductStockInfo.as_view(),name='productstockinfo')


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
