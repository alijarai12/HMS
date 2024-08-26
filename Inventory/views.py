from django.shortcuts import render
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework.views import APIView
from HMS.CustomPagination import CustomPagination
from Core.permissions import *
from Core.utils import *
from rest_framework.generics import GenericAPIView
from custom_response.response import CustomResponse
from Core.mixins import *

# Create your views here.

class SupplierTypeList(HotelFilterMixin,GenericAPIView):
    """ This class lists and creates the SupplierTypeList """
    permission_classes = [CustomModelPermission]
    queryset_model = SupplierType
    pagination_class = CustomPagination()
    search_fields = ['type']
    filterset_fields = ['hotel_id', 'id']

    def get(self, request):
        response = CustomResponse()
        querysets_items = SupplierType.objects.all()
        supplier_type = self.filter_queryset(self.filter_by_hotel(querysets_items))
        if supplier_type:
            paginator = self.pagination_class
            paginated_queryset = paginator.paginate_queryset(supplier_type, request)

            serializer = GetSupplierTypeSerializer(paginated_queryset, many=True)
            response_data = {
                'next': paginator.get_next_link(),
                'previous': paginator.get_previous_link(),
                'count': paginator.page.paginator.count,    
                'data': serializer.data
            }
            return Response(response.successResponse("SupplierType data view successfully", response_data), status=status.HTTP_200_OK)
        return Response(response.errorResponse('No data found'), status=status.HTTP_404_NOT_FOUND)


    def post(self, request):
        serializer = SupplierTypeSerializer(data=request.data)
        response = CustomResponse()
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("SupplierType Added successfully", serializer.data), status=status.HTTP_201_CREATED)
        return Response(response.errorResponse("Validation Error", serializer.errors), status=status.HTTP_400_BAD_REQUEST)



class SupplierTypeDetail(GetObjectMixin, APIView):
    permission_classes = [HotelAssociatedObj, CustomModelPermission]
    queryset_model = SupplierType
    filterset_fields = ['hotel_id', 'id']

    # def get_queryset_object(self, pk):
    #     try:
    #         return SupplierType.objects.get(pk=pk)
    #     except SupplierType.DoesNotExist:
    #         return None
        
    def get(self,request, pk):
        supplier_type = self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not supplier_type:
           return Response(response.errorResponse('Data is not found,'),status=status.HTTP_404_NOT_FOUND)
        serializer=GetSupplierTypeSerializer(supplier_type)
        return Response(response.successResponse('SupplierType Details',serializer.data),status=status.HTTP_200_OK)
    

    def put(self, request, pk):
        supplier_type=self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not supplier_type:
           return Response(response.errorResponse('Data is not found,'),status=status.HTTP_404_NOT_FOUND)
        serializer=SupplierTypeSerializer(supplier_type,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("SupplierType Updated Successfully", serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse("Bad Request", serializer.errors), status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, pk):
        supplier_type=self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not supplier_type:
           return Response(response.errorResponse('Data is not found,'),status=status.HTTP_404_NOT_FOUND)        
        supplier_type.delete()
        return Response(response.errorResponse("Deleted Successfully"), status=status.HTTP_204_NO_CONTENT)




class SupplierList(HotelFilterMixin,GenericAPIView):
    """ This class lists and creates the SupplierTypeList """
    permission_classes = [CustomModelPermission]
    queryset_model = Supplier
    pagination_class = CustomPagination()
    search_fields = ['name','address','contact_no']
    filterset_fields = ['type','hotel_id', 'id']

    def get(self, request):
        response = CustomResponse()
        querysets_items = Supplier.objects.all()
        supplier = self.filter_queryset(self.filter_by_hotel(querysets_items))
        if supplier:
            paginator = self.pagination_class
            paginated_queryset = paginator.paginate_queryset(supplier, request)

            serializer = GetSupplierSerializer(paginated_queryset, many=True)
            response_data = {
                'next': paginator.get_next_link(),
                'previous': paginator.get_previous_link(),
                'count': paginator.page.paginator.count,
                'data': serializer.data
            }
            return Response(response.successResponse("Supplier data view successfully", response_data), status=status.HTTP_200_OK)
        return Response(response.errorResponse('No data found'), status=status.HTTP_404_NOT_FOUND)
        

    def post(self, request):
        serializer = SupplierSerializer(data=request.data)
        response = CustomResponse()
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("Supplier Added successfully", serializer.data), status=status.HTTP_201_CREATED)
        return Response(response.errorResponse("Validation Error", serializer.errors), status=status.HTTP_400_BAD_REQUEST)



class SupplierDetail(GetObjectMixin, GenericAPIView):
    permission_classes = [HotelAssociatedObj, CustomModelPermission]
    queryset_model = Supplier
    filterset_fields = ['hotel_id', 'id']
    search_fields = ['name']

    # def get_queryset_object(self, pk):
    #     try:
    #         return Supplier.objects.get(pk=pk)
    #     except Supplier.DoesNotExist:
    #         return None
        
    def get(self,request, pk):
        supplier = self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not supplier:
           return Response(response.errorResponse('Data is not found,'),status=status.HTTP_404_NOT_FOUND)
        serializer=GetSupplierSerializer(supplier)
        return Response(response.successResponse('Supplier Details',serializer.data),status=status.HTTP_200_OK)
    

    def put(self, request, pk):
        supplier=self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not supplier:
           return SupplierSerializer(response.errorResponse('Data is not found,'),status=status.HTTP_404_NOT_FOUND)
        serializer=SupplierSerializer(supplier,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("Supplier Updated Successfully", serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse("Bad Request", serializer.errors), status=status.HTTP_400_BAD_REQUEST)

    
    
    def delete(self, request, pk):
        supplier=self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not supplier:
           return Response(response.errorResponse('Data is not found,'),status=status.HTTP_404_NOT_FOUND)        
        supplier.delete()
        return Response(response.errorResponse("Deleted Successfully"), status=status.HTTP_204_NO_CONTENT)




class ProductCategoryList(HotelFilterMixin,GenericAPIView):
    """ This class lists and creates the ProductCategoryList """
    permission_classes = [CustomModelPermission]
    queryset_model = ProductCategory
    pagination_class = CustomPagination()
    search_fields = ['name','description']
    filterset_fields = ['hotel_id']

    def get(self, request):
        response = CustomResponse()
        querysets_items = ProductCategory.objects.all().order_by('id')
        productcategory = self.filter_queryset(self.filter_by_hotel(querysets_items))
        if productcategory:
            paginator = self.pagination_class
            paginated_queryset = paginator.paginate_queryset(productcategory, request)

            serializer = GetProductCategorySerializer(paginated_queryset, many=True)
            response_data = {
                'next': paginator.get_next_link(),
                'previous': paginator.get_previous_link(),
                'count': paginator.page.paginator.count,
                'data': serializer.data
            }
            return Response(response.successResponse("ProductCategory data view successfully", response_data), status=status.HTTP_200_OK)
        return Response(response.errorResponse('No data found'), status=status.HTTP_404_NOT_FOUND)
        
       

    def post(self, request):
        serializer = ProductCategorySerializer(data=request.data)
        response = CustomResponse()
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("ProductCategory Added successfully", serializer.data), status=status.HTTP_201_CREATED)
        return Response(response.errorResponse("Validation Error", serializer.errors), status=status.HTTP_400_BAD_REQUEST)



class ProductCategoryDetail(GetObjectMixin, APIView):
    permission_classes = [HotelAssociatedObj, CustomModelPermission]
    queryset_model = ProductCategory
    filterset_fields = ['id', 'hotel_id']
    search_fields = ['name']

    # def get_queryset_object(self, pk):
        # try:
        #     return ProductCategory.objects.get(pk=pk)
        # except ProductCategory.DoesNotExist:
        #     return None
        
    def get(self,request, pk):
        productcategory = self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not productcategory:
           return Response(response.errorResponse('Data is not found,'),status=status.HTTP_404_NOT_FOUND)
        serializer=GetProductCategorySerializer(productcategory)
        return Response(response.successResponse('ProductCategoryList Details',serializer.data),status=status.HTTP_200_OK)



    def put(self, request, pk):
        productcategory=self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not productcategory:
           return Response(response.errorResponse('Data is not found,'),status=status.HTTP_404_NOT_FOUND)
        serializer=ProductCategorySerializer(productcategory,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("ProductCategoryList Updated Successfully", serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse("Bad Request", serializer.errors), status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, pk):
        productcategory=self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not productcategory:
           return Response(response.errorResponse('Data is not found,'),status=status.HTTP_404_NOT_FOUND)        
        productcategory.delete()
        return Response(response.errorResponse("Deleted Successfully"), status=status.HTTP_204_NO_CONTENT)



class ProductList(HotelFilterMixin,GenericAPIView):
    """ This class lists and creates the ProductList """
    permission_classes = [CustomModelPermission]
    queryset_model = Product
    pagination_class = CustomPagination()
    search_fields = ['status','brand','product_name','product_unit']
    filterset_fields = ['category','department','hotel_id']
    
    def get(self, request):
        response = CustomResponse()
        querysets_items = Product.objects.all()
        product = self.filter_queryset(self.filter_by_hotel(querysets_items))
        if product:
            paginator = self.pagination_class
            paginated_queryset = paginator.paginate_queryset(product, request)
            
            serializer = GetProductSerializer(paginated_queryset, many=True)
            response_data = {
                'next': paginator.get_next_link(),
                'previous': paginator.get_previous_link(),
                'count': paginator.page.paginator.count,
                'data': serializer.data
            }
            return Response(response.successResponse("Product data view successfully", response_data), status=status.HTTP_200_OK)
        return Response(response.errorResponse('No data found'), status=status.HTTP_404_NOT_FOUND)


        

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        
        response = CustomResponse()
        
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("Product Added successfully", serializer.data), status=status.HTTP_201_CREATED)
        return Response(response.errorResponse("Validation Error", serializer.errors), status=status.HTTP_400_BAD_REQUEST)



class ProductDetail(GetObjectMixin, APIView):
    permission_classes = [HotelAssociatedObj, CustomModelPermission]
    queryset_model = Product
    filterset_fields = ['id', 'hotel_id', 'brand']
    search_fields = ['product_name', 'status']

    # def get_queryset_object(self, pk):
    #     try:
    #         return Product.objects.get(pk=pk)
    #     except Product.DoesNotExist:
    #         return None
        
    def get(self,request, pk):
        product = self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not product:
           return Response(response.errorResponse('Data is not found,','Not Found'),status=status.HTTP_404_NOT_FOUND)
        serializer=GetProductSerializer(product)

        return Response(response.successResponse('Product Details',serializer.data),status=status.HTTP_200_OK)


    def put(self, request, pk):
        product=self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not product:
           return ProductSerializer(response.errorResponse('Data is not found,'),status=status.HTTP_404_NOT_FOUND)
        serializer=ProductSerializer(product,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("Product Updated Successfully", serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse("Bad Request", serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, pk):
        product=self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not product:
           return Response(response.errorResponse('Data is not found,'),status=status.HTTP_404_NOT_FOUND)        
        product.delete()
        return Response(response.errorResponse("Product Deleted Successfully"), status=status.HTTP_204_NO_CONTENT)



class PurchaseOrder(HotelFilterMixin,GenericAPIView):
    """ This class lists and creates the PurchaseOrderList """
    permission_classes = [CustomModelPermission]
    queryset_model = PurchaseOrderList
    pagination_class = CustomPagination()
    search_fields = ['status','remark']
    filterset_fields = ['supplier__id', 'hotel_id', 'id']

    def get(self, request):
        response = CustomResponse()
        querysets_items = PurchaseOrderList.objects.prefetch_related('purchaseorderitems').all()
        purchaseorderlist = self.filter_queryset(self.filter_by_hotel(querysets_items))
        if purchaseorderlist:
            paginator = self.pagination_class

            paginated_queryset = paginator.paginate_queryset(purchaseorderlist, request)

            serializer = GetPurchaseOrderListSerializer(paginated_queryset, many=True)
            response_data = {
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'count': paginator.page.paginator.count,
            'data': serializer.data           
        }
            return Response(response.successResponse("PurchaseOrderList data view successfully", response_data), status=status.HTTP_200_OK)
        return Response(response.errorResponse('No data found'), status=status.HTTP_404_NOT_FOUND)

        


    def post(self, request):
        hotel_id = request.user.hotel_id.id
        request.data['hotel_id'] = hotel_id
        purchase_items = request.data.get('purchase_items')
        discount_perc = request.data.get('discount_perc')
        tax_perc = request.data.get('tax_perc')
        total = 0
        serializer = PurchaseOrderListSerializer(data=request.data)
        response = CustomResponse()
        if serializer.is_valid():
            a = serializer.save()
            for i in purchase_items:
                unit_price = i.get('unit_price')
                quantity = i.get('quantity')
                subtotal = int(quantity) * int(unit_price)
                i['subtotal'] = subtotal
                total += subtotal
                i['purchase_order_list'] = a.id
                i['hotel_id'] = hotel_id
                purchase_order_item = PurchaseOrderItemsSerializer(data=i)
                if purchase_order_item.is_valid():
                    purchase_order_item.save()
                else:
                    return Response(response.errorResponse("Validation Error", purchase_order_item.errors), status=status.HTTP_400_BAD_REQUEST)
            discount_amount = total * int(discount_perc) / 100
            tax_amount = total * int(tax_perc) / 100
            discounted_amount = total - discount_amount + tax_amount
            a.total = discounted_amount
            a.discount = discounted_amount
            a.tax = tax_amount 
            a.save()
            return Response(response.successResponse("PurchaseOrderList Added successfully", serializer.data), status=status.HTTP_201_CREATED)
        return Response(response.errorResponse("Validation Error", serializer.errors), status=status.HTTP_400_BAD_REQUEST)



class PurchaseOrderListDetail(GetObjectMixin, APIView):
    permission_classes = [HotelAssociatedObj, CustomModelPermission]
    queryset_model = PurchaseOrderList
    filterset_fields = ['supplier__id', 'id', 'hotel_id', ]

    # def get_queryset_object(self, pk):
    #     try:
    #         return PurchaseOrderList.objects.get(pk=pk)
    #     except PurchaseOrderList.DoesNotExist:
    #         return None
        
    def get(self,request, pk):
        purchaseorderlist = self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not purchaseorderlist:
           return Response(response.errorResponse('Data is not found,'),status=status.HTTP_404_NOT_FOUND)
        serializer=GetPurchaseOrderListSerializer(purchaseorderlist)
        return Response(response.successResponse('PurchaseOrderList Details',serializer.data),status=status.HTTP_200_OK)



    def put(self, request, pk):
        purchaseorderlist=self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not purchaseorderlist:
           return PurchaseOrderListSerializer(response.errorResponse('Data is not found,'),status=status.HTTP_404_NOT_FOUND)
        serializer=PurchaseOrderListSerializer(purchaseorderlist,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("PurchaseOrderList Updated Successfully", serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse("Bad Request", serializer.errors), status=status.HTTP_400_BAD_REQUEST)


    
    def delete(self, request, pk):
        purchaseorderlist=self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not purchaseorderlist:
           return Response(response.errorResponse('Data is not found,'),status=status.HTTP_404_NOT_FOUND)        
        purchaseorderlist.delete()
        return Response(response.errorResponse("PurchaseOrderList Deleted Successfully"), status=status.HTTP_204_NO_CONTENT)



class PurchaseOrderItemsList(HotelFilterMixin,GenericAPIView):
    """ This class lists and creates the PurchaseOrderItems List """
    permission_classes = [CustomModelPermission]
    queryset_model = PurchaseOrderItems
    pagination_class = CustomPagination()
    filterset_fields = ['product','purchase_order_list','hotel_id']

    def get(self, request):
        response = CustomResponse()
        querysets_items = PurchaseOrderItems.objects.all()
        purchaseorderitem = self.filter_queryset(self.filter_by_hotel(querysets_items))
        if purchaseorderitem:
            paginator = self.pagination_class

            paginated_queryset = paginator.paginate_queryset(purchaseorderitem, request)

            serializer = GetPurchaseOrderItemsSerializer(paginated_queryset, many=True)
            response_data = {
                'next': paginator.get_next_link(),
                'previous': paginator.get_previous_link(),
                'count': paginator.page.paginator.count,
                'data': serializer.data
            }
            return Response(response.successResponse("PurchaseOrderItems data view successfully", response_data), status=status.HTTP_200_OK)
        return Response(response.errorResponse('No data found'), status=status.HTTP_404_NOT_FOUND)
        


    def post(self, request):
        serializer = PurchaseOrderItemsSerializer(data=request.data)
        response = CustomResponse()
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("PurchaseOrderItems Added successfully", serializer.data), status=status.HTTP_201_CREATED)
        return Response(response.errorResponse("Validation Error", serializer.errors), status=status.HTTP_400_BAD_REQUEST)



class PurchaseOrderItemsDetail(GetObjectMixin, APIView):
    permission_classes = [HotelAssociatedObj, CustomModelPermission]
    queryset_model = PurchaseOrderItems
    filterset_fields = ['product__id', 'purchase_order_list__id', 'id', 'hotel_id']

    # def get_queryset_object(self, pk):
    #     try:
    #         return PurchaseOrderItems.objects.get(pk=pk)
    #     except PurchaseOrderItems.DoesNotExist:
    #         return None
        
    def get(self,request, pk):
        purchaseorderitem = self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not purchaseorderitem:
           return Response(response.errorResponse('Data is not found,','Not Found'),status=status.HTTP_404_NOT_FOUND)
        serializer=GetPurchaseOrderItemsSerializer(purchaseorderitem)

        return Response(response.successResponse('StockItem Details',serializer.data),status=status.HTTP_200_OK)



    def put(self, request, pk):
        purchaseorderitem=self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not purchaseorderitem:
           return PurchaseOrderItemsSerializer(response.errorResponse('Data is not found,','Not Found'),status=status.HTTP_404_NOT_FOUND)
        serializer=PurchaseOrderItemsSerializer(purchaseorderitem,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("StockItem Updated Successfully", serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse("Bad Request", serializer.errors), status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, pk):
        purchaseorderitem=self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not purchaseorderitem:
           return Response(response.errorResponse('Data is not found,'),status=status.HTTP_404_NOT_FOUND)        
        purchaseorderitem.delete()
        return Response(response.errorResponse("StockItem Deleted Successfully"), status=status.HTTP_204_NO_CONTENT)



class StoreRequestList(HotelFilterMixin,GenericAPIView):
    """ This class lists and creates the StoreRequestList """
    permission_classes = [CustomModelPermission]
    queryset_model = StoreRequest
    pagination_class = CustomPagination()
    search_fields = ['status']
    filterset_fields = ['requesting_department','products','hotel_id']

    def get(self, request):
        response = CustomResponse()
        querysets_items = StoreRequest.objects.all().order_by('id')
        storerequest = self.filter_queryset(self.filter_by_hotel(querysets_items))
        if storerequest:
            paginator = self.pagination_class

            paginated_queryset = paginator.paginate_queryset(storerequest, request)

            serializer = GetStoreRequestSerializer(paginated_queryset, many=True)
            response_data = {
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'count': paginator.page.paginator.count,
            'data': serializer.data
         }
            return Response(response.successResponse("StoreRequestList data view successfully", response_data), status=status.HTTP_200_OK)
        return Response(response.errorResponse('No data found'), status=status.HTTP_404_NOT_FOUND)
        

    def post(self, request):
        serializer = StoreRequestSerializer(data=request.data)
        response = CustomResponse()
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("StoreRequestList Added successfully", serializer.data), status=status.HTTP_201_CREATED)
        return Response(response.errorResponse("Validation Error", serializer.errors), status=status.HTTP_400_BAD_REQUEST)



class StoreRequestDetail(GetObjectMixin, APIView):
    permission_classes = [HotelAssociatedObj, CustomModelPermission]
    queryset_model = StoreRequest
    filterset_fields = ['hotel_id','id', 'product__id']
    search_fields = ['status'] 

    # def get_queryset_object(self, pk):
    #     try:
    #         return StoreRequest.objects.get(pk=pk)
    #     except StoreRequest.DoesNotExist:
    #         return None
        
    def get(self,request, pk):
        storerequest = self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not storerequest:
           return Response(response.errorResponse('Data is not found,','Not Found'),status=status.HTTP_404_NOT_FOUND)
        serializer=GetStoreRequestSerializer(storerequest)

        return Response(response.successResponse('StoreRequestList Details',serializer.data),status=status.HTTP_200_OK)



    def put(self, request, pk):
        storerequest=self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not storerequest:
           return StoreRequestSerializer(response.errorResponse('Data is not found,','Not Found'),status=status.HTTP_404_NOT_FOUND)
        serializer=StoreRequestSerializer(storerequest,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("StoreRequestList Updated Successfully", serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse("Bad Request", serializer.errors), status=status.HTTP_400_BAD_REQUEST)


    
    def delete(self, request, pk):
        storerequest=self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not storerequest:
           return Response(response.errorResponse('Data is not found,'),status=status.HTTP_404_NOT_FOUND)        
        storerequest.delete()
        return Response(response.errorResponse("StoreRequestList Deleted Successfully"), status=status.HTTP_204_NO_CONTENT)




class ReturnProductDetailsList(HotelFilterMixin,GenericAPIView):
    """ This class lists and creates the ReturnProductDetails List """
    permission_classes = [CustomModelPermission]
    queryset_model = ReturnProductDetails
    pagination_class = CustomPagination()
    search_fields = ['reason']
    filterset_fields = ['purchase_order_item__id','hotel_id', 'id']

    def get(self, request):
        response = CustomResponse()
        querysets_items = ReturnProductDetails.objects.all()
        return_product_detail = self.filter_queryset(self.filter_by_hotel(querysets_items))
        if return_product_detail:
            paginator = self.pagination_class

            paginated_queryset = paginator.paginate_queryset(return_product_detail, request)

            serializer = GetReturnProductDetailsSerializer(paginated_queryset, many=True)
            response_data = {
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'count': paginator.page.paginator.count,
            'data': serializer.data
           }
            return Response(response.successResponse("ReturnProductDetails data view successfully", response_data), status=status.HTTP_200_OK)
        return Response(response.errorResponse('No data found'), status=status.HTTP_404_NOT_FOUND)



    def post(self, request):
        serializer = ReturnProductDetailsSerializer(data=request.data)
        response = CustomResponse()
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("ReturnProductDetails Added successfully", serializer.data), status=status.HTTP_201_CREATED)
        return Response(response.errorResponse("Validation Error", serializer.errors), status=status.HTTP_400_BAD_REQUEST)



class ReturnProduct(GetObjectMixin, APIView):
    permission_classes = [HotelAssociatedObj, CustomModelPermission]
    queryset_model = ReturnProductDetails
    filterset_fields = ['hotel_id','order','guest','restaurant_transaction']
    search_fields = ['reason']

    # def get_queryset_object(self, pk):
    #     try:
    #         return ReturnProductDetails.objects.get(pk=pk)
    #     except ReturnProductDetails.DoesNotExist:
    #         return None
        
    def get(self,request, pk):
        return_product_detail = self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not return_product_detail:
           return Response(response.errorResponse('Data is not found,'),status=status.HTTP_404_NOT_FOUND)
        serializer=GetReturnProductDetailsSerializer(return_product_detail)

        return Response(response.successResponse('ReturnProductDetails Details',serializer.data),status=status.HTTP_200_OK)



    def put(self, request, pk):
        return_product_detail=self.get_queryset_object(self.queryset_model,pk)
        response=CustomResponse()
        if not return_product_detail:
           return ReturnProductDetailsSerializer(response.errorResponse('Data is not found,'),status=status.HTTP_404_NOT_FOUND)
        serializer=ReturnProductDetailsSerializer(return_product_detail, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("ReturnProductDetails Updated Successfully", serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse("Bad Request", serializer.errors), status=status.HTTP_400_BAD_REQUEST)

    
    
    def delete(self, request, pk):
        return_product_detail=self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not return_product_detail:
           return Response(response.errorResponse('Data is not found,','Not Found'),status=status.HTTP_404_NOT_FOUND)        
        return_product_detail.delete()
        return Response(response.errorResponse("ReturnProductDetails Deleted Successfully"), status=status.HTTP_204_NO_CONTENT)



class ProductStockInfo(GenericAPIView):
    serializer_class = GetProductStockInfoSerializer
    filterset_fields = ['hotel_id', 'id']
    search_fields = ['product_name', 'brand', ]


    def get(self,requset):
        product_objects = Product.objects.filter(hotel_id=requset.user.hotel_id)
        serializer = self.serializer_class(product_objects,many=True)
        response = CustomResponse()
        return Response(response.successResponse("Product Stock Info List", serializer.data), status=status.HTTP_200_OK)

