from rest_framework import serializers
from .models import *
from Employee.serializers import *
from django.db.models import Sum

class GetSupplierTypeSerializer(serializers.ModelSerializer):
    # hotel_id=HotelSerializer()
    class Meta:
        model = SupplierType
        # fields = '__all__'
        exclude = ['hotel_id']


class SupplierTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierType
        fields = '__all__'



class GetSupplierSerializer(serializers.ModelSerializer):
    # hotel_id = HotelSerializer()
    type = SupplierTypeSerializer()

    class Meta:
        model = Supplier
        # fields = '__all__'
        exclude = ['hotel_id']

class SupplierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Supplier
        fields = '__all__'


class GetProductCategorySerializer(serializers.ModelSerializer):
    # hotel_id = HotelSerializer()
    
    class Meta:
        model = ProductCategory
        # fields = '__all__'
        exclude = ['hotel_id']

class ProductCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCategory
        fields = '__all__'


class GetProductSerializer(serializers.ModelSerializer):
    # hotel_id = HotelSerializer()
    category = ProductCategorySerializer()
    
    class Meta:
        model = Product
        # fields = '__all__'
        exclude = ['hotel_id']

class GetMinProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = ['id','product_name','quantity','product_unit']


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'





# class GetStockItemSerializer(serializers.ModelSerializer):
#     hotel_id = HotelSerializer()
#     products = ProductSerializer()

#     class Meta:
#         model = StockItem
#         fields = '__all__'

# class StockItemSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = StockItem
#         fields = [ 'id', 'products', 'quantity', 'stock_list', 'hotel_id','updated_at', 'created_at']


class GetPurchaseOrderItemsSerializer(serializers.ModelSerializer):
    # hotel_id = HotelSerializer()
    product = ProductSerializer()
    # purchase_order_list = PurchaseOrderListSerializer()
    # purchase_order_list = GetPurchaseOrderListSerializer()

    class Meta:
        model = PurchaseOrderItems
        # fields = '__all__'
        exclude = ['hotel_id']

class PurchaseOrderItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = PurchaseOrderItems
        fields = '__all__'


    
class GetPurchaseOrderListSerializer(serializers.ModelSerializer):
    # hotel_id = HotelSerializer()
    supplier = SupplierSerializer()
    purchaseorderitems = GetPurchaseOrderItemsSerializer(many = True)

    class Meta:
        model = PurchaseOrderList
        fields = ['id','supplier', 'discount_perc', 'discount', 'remark', 'tax_perc', 'tax', 'status', 'created_at', 'updated_at', 'total', 'purchaseorderitems']
        


class PurchaseOrderListSerializer(serializers.ModelSerializer):

    class Meta:
        model = PurchaseOrderList
        fields = '__all__'




class GetStoreRequestSerializer(serializers.ModelSerializer):
    # hotel_id = HotelSerializer()
    products = ProductSerializer()
    requesting_department = DepartmentSerializer()

    class Meta:
        model = StoreRequest
        # fields = '__all__'
        exclude = ['hotel_id']

class StoreRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = StoreRequest
        fields = '__all__'


# class LimitedPurchaseOrderListSerializer(serializers.ModelSerializer):
#     supplier = SupplierSerializer()

#     class Meta:
#         model = PurchaseOrderList
#         fields = ['supplier']


# class GetPPurchaseOrderItemsSerializer(serializers.ModelSerializer):
#     # hotel_id = HotelSerializer()
#     # product = ProductSerializer()
#     purchase_order_list = LimitedPurchaseOrderListSerializer()

#     class Meta:
#         model = PurchaseOrderItems
#         fields = '__all__'


# class GetReturnProductDetailsSerializer(serializers.ModelSerializer):
#     hotel_id = HotelSerializer()
#     # purchase_order_item = PurchaseOrderItemsSerializer()
#     purchase_order_item = GetPPurchaseOrderItemsSerializer()

#     class Meta:
#         model = ReturnProductDetails
#         fields = '__all__'


class GetReturnProductDetailsSerializer(serializers.ModelSerializer):
    # purchase_order_item = PurchaseOrderItemsSerializer()
    purchase_order_item = GetPurchaseOrderItemsSerializer()

    class Meta:
        model = ReturnProductDetails
        # fields = '__all__'
        exclude = ['hotel_id']


class ReturnProductDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReturnProductDetails
        fields = '__all__'

    
class GetSupplierQuantityInfoSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='purchase_order_list.supplier.name')
    class Meta:
        model = PurchaseOrderItems
        fields = ['id','supplier_name','quantity']


class GetProductStockInfoSerializer(serializers.ModelSerializer):
    supplier_info = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id','quantity','status','product_name','image','supplier_info']
    
    def get_supplier_info(self,instance):
        total_supplier_info = instance.purchaseorderitems.all()
        serializer = GetSupplierQuantityInfoSerializer(total_supplier_info,many=True)
        return serializer.data






