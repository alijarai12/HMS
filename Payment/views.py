from .models import *
from Core.utils import *
from Core .mixins import *
from .serializers import *
from Core.permissions import *
from rest_framework import status
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from HMS.CustomPagination import CustomPagination
from rest_framework.generics import GenericAPIView
from custom_response.response import CustomResponse


class PaymentMethodList(HotelFilterMixin,GenericAPIView):
    """ This class lists and creates the PaymentMethodList """
    permission_classes = [CustomModelPermission]
    queryset_model = PaymentMethod
    pagination_class = CustomPagination()
    search_fields = ['name','payment_detail']
    filterset_fields = ['hotel_id']

    def get(self, request):
        querysets_items = PaymentMethod.objects.all()
        methods = self.filter_queryset(self.filter_by_hotel(querysets_items))
        response = CustomResponse()

        if methods:
            paginator = self.pagination_class
            paginated_queryset = paginator.paginate_queryset(methods, request)
            serializer = GetPaymentMethodSerializer(paginated_queryset, many=True)
            response_data = {
                'next': paginator.get_next_link(),
                'previous': paginator.get_previous_link(),
                'count': paginator.page.paginator.count,                 
                'data': serializer.data
            }
            return Response(response.successResponse("data view", response_data), status=status.HTTP_200_OK)
        else:
            return Response(response.errorResponse('No data found'), status=status.HTTP_404_NOT_FOUND)
 
    
    
    def post(self, request, format=None):
        serializer = PaymentMethodSerializer(data=request.data)
        response=CustomResponse()
        
        if serializer.is_valid():
            serializer.save()
            response_data = {
            'data': serializer.data
        }

            return Response(response.successResponse('data created',response_data), status=status.HTTP_201_CREATED)
        return Response(response.errorResponse('Error Occured',serializer.errors), status=status.HTTP_400_BAD_REQUEST)



class PaymentMethodDetail(GetObjectMixin, APIView):
    permission_classes = [HotelAssociatedObj, CustomModelPermission]
    queryset_model = PaymentMethod

        
    def put(self, request, pk):
        method=self.get_queryset_object(self.queryset_model ,pk)
        response=CustomResponse()
        if not method:
           return Response(response.errorResponse('Data is not found'),status=status.HTTP_404_NOT_FOUND)
        serializer=PaymentMethodSerializer(method,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("Payment method Updated Successfully", serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse("Bad Request", serializer.errors), status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, pk):
        method=self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not method:
           return Response(response.errorResponse('Data is not found'),status=status.HTTP_404_NOT_FOUND)        
        method.delete()
        return Response(response.errorResponse("Deleted Successfully"), status=status.HTTP_204_NO_CONTENT)
    


class BankInfoList(HotelFilterMixin,GenericAPIView):
    """ This class lists and creates the BankInfoList """
    permission_classes = [CustomModelPermission]
    queryset_model = BankInfo
    pagination_class = CustomPagination()
    search_fields = ['bank_name','bank_branch','bank_account_no']
    filterset_fields = ['hotel_id']
    

    def get(self, request):
        response = CustomResponse()
        querysets_items = BankInfo.objects.all()
        print(querysets_items)
        bank_infos = self.filter_queryset(self.filter_by_hotel(querysets_items))
        if bank_infos:
            paginator = self.pagination_class
            paginated_queryset = paginator.paginate_queryset(bank_infos, request)

            serializer = GetBankInfoSerializer(paginated_queryset, many=True)
            response_data = {
                'next': paginator.get_next_link(),
                'previous': paginator.get_previous_link(),
                'count': paginator.page.paginator.count,    
                'data': serializer.data
            }

            return Response(response.successResponse("data view", response_data), status=status.HTTP_200_OK)
        else:
            return Response(response.errorResponse('No data found'), status=status.HTTP_404_NOT_FOUND)

    
    
    def post(self, request, format=None):
        serializer = BankInfoSerializer(data=request.data)
        response=CustomResponse()
        
        if serializer.is_valid():
            serializer.save()
            response_data = {
            'data': serializer.data
        }

            return Response(response.successResponse('data created',response_data), status=status.HTTP_201_CREATED)
        return Response(response.errorResponse('Error Occured',serializer.errors), status=status.HTTP_400_BAD_REQUEST)



class BankInfoDetail(GetObjectMixin, GenericAPIView):
    permission_classes = [HotelAssociatedObj,CustomModelPermission]
    queryset_model = BankInfo

    # def get_queryset_object(self, pk):
    #     try:
    #         return BankInfo.objects.get(pk=pk)
    #     except BankInfo.DoesNotExist:
    #         return None
        
    def get(self,request, pk):
        bank_info= self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not bank_info:
           return Response(response.errorResponse('Data is not found'),status=status.HTTP_404_NOT_FOUND)
        serializer=GetBankInfoSerializer(bank_info)
        return Response(response.successResponse('Bank Info Method Details',serializer.data),status=status.HTTP_200_OK)

    def put(self, request, pk):
        bank_info=self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not bank_info:
           return Response(response.errorResponse('Data is not found,'),status=status.HTTP_404_NOT_FOUND)
        serializer=BankInfoSerializer(bank_info,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("Payment method Updated Successfully", serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse("Bad Request", serializer.errors), status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, pk):
        bank_info=self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not bank_info:
           return Response(response.errorResponse('Data is not found,','Not Found'),status=status.HTTP_404_NOT_FOUND)        
        bank_info.delete()
        return Response(response.errorResponse("Deleted Successfully"), status=status.HTTP_204_NO_CONTENT)
    
    