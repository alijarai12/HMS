from .models import *
from Core.utils import *
from .serializers import *
from Core.permissions import *
from rest_framework import status
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from HMS.CustomPagination import CustomPagination
from rest_framework.generics import GenericAPIView
from custom_response.response import CustomResponse
from Core.mixins import *


class ExpenseListView(HotelFilterMixin,GenericAPIView):
    permission_classes = [CustomModelPermission]
    queryset_model = Expense
    pagination_class = CustomPagination()
    search_fields = ['expense_name','expense_desc']
    filterset_fields = ['hotel_id','department']

    def get(self, request):
        response = CustomResponse()
        explist_querysets = Expense.objects.all()
        expense_list = self.filter_queryset(self.filter_by_hotel(explist_querysets))
        if expense_list:
            paginator = self.pagination_class
            paginated_queryset = paginator.paginate_queryset(expense_list, request)
            serializer = GetExpenseSerializer(paginated_queryset, many=True)
            response_data = {
                'next': paginator.get_next_link(),
                'previous': paginator.get_previous_link(),
                'count': paginator.page.paginator.count,
                "data":serializer.data
            }
            return Response(response.successResponse('data view', response_data), status=status.HTTP_200_OK)
        return Response(response.errorResponse('No data found'), status=status.HTTP_404_NOT_FOUND)

    
    def post(self, request):
         serializer = ExpenseSerializer(data=request.data)
         response = CustomResponse()
         if serializer.is_valid():
             serializer.save()
             return Response(response.successResponse('Expense data created successfilly', serializer.data), status=status.HTTP_201_CREATED)
         return Response(response.errorResponse("Validation error!", serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    
    

class ExpenseDetailsView(GetObjectMixin, APIView):
    permission_classes = [HotelAssociatedObj, CustomModelPermission]
    queryset_model = Expense
    filterset_fields = ['id', 'hotel_id']
    search_fields = ['expense_name']

    # def get_queryset_object(self, pk):
    #     try:
    #         return Expense.objects.get(pk=pk)
    #     except Expense.DoesNotExist:
    #         return None
        
    def get(self, request, pk):
        exp_details = self.get_queryset_object(self.queryset_model, pk)
        response = CustomResponse()
        if not exp_details:
            return Response(response.errorResponse("Data not found", "Not Found"), status=status.HTTP_404_NOT_FOUND)
        serializer = GetExpenseSerializer(exp_details)
        return Response(response.successResponse("Expense details loaded successfully", serializer.data), status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        exp_details = self.get_queryset_object(self.queryset_model,pk)
        response = CustomResponse()
        if not exp_details:
            return Response(response.errorResponse(404, "Data not found", "Not Found"), status=status.HTTP_404_NOT_FOUND)
        serializer = ExpenseSerializer(exp_details, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("Data updated successfully", serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse('Validation Error!', serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        exp_details = self.get_queryset_object(self.queryset_model,pk)
        response = CustomResponse()
        if not exp_details:
            return Response(response.errorResponse("Data not found", "Not Found"), status=status.HTTP_404_NOT_FOUND)
        exp_details.delete()
        return Response(response.errorResponse("Data deleted successfully"), status=status.HTTP_204_NO_CONTENT)
    

class ExpenseStatusListView(HotelFilterMixin,GenericAPIView):
    permission_classes = [CustomModelPermission]
    queryset_model = ExpenseStatus
    pagination_class = CustomPagination()
    search_fields = ['status']
    filterset_fields = ['hotel_id','expense','accepted_by']

    def get(self, request):
        response = CustomResponse()
        expstat_qyerysets = ExpenseStatus.objects.all()
        expstatus_list = self.filter_queryset(self.filter_by_hotel(expstat_qyerysets))
        if expstatus_list:
            paginator = self.pagination_class
            paginated_queryset = paginator.paginate_queryset(expstatus_list, request)
            serializer = GetExpenseStatusSerializer(paginated_queryset, many=True)
            response_data = {
                'next': paginator.get_next_link(),
                'previous': paginator.get_previous_link(),
                'count': paginator.page.paginator.count,
                "data":serializer.data
            }
            return Response(response.successResponse('data view', response_data), status=status.HTTP_200_OK)
        return Response(response.errorResponse('No data found'), status=status.HTTP_404_NOT_FOUND)

    
    def post(self, request):
        serializer = ExpenseStatusSerializer(data=request.data)
        response = CustomResponse()
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("Expense status data added", serializer.data), status=status.HTTP_201_CREATED)
        return Response(response.errorResponse("Validation error", serializer.errors), status=status.HTTP_400_BAD_REQUEST)



class ExpenseStatusDetailView(GetObjectMixin, APIView):
    permission_classes = [HotelAssociatedObj, CustomModelPermission]
    queryset_model = ExpenseStatus
    filterset_fields = ['id', 'hotel_id']

    # def get_queryset_object(self, pk):
    #     try:
    #         return ExpenseStatus.objects.get(pk=pk)
    #     except ExpenseStatus.DoesNotExist:
    #         return None
        
    def get(self, request, pk):
        exp_status = self.get_queryset_object(pk)
        response = CustomResponse()
        if not exp_status:
            return Response(response.errorResponse("Data not found"), status=status.HTTP_404_NOT_FOUND)
        serializer = GetExpenseStatusSerializer(exp_status)
        return Response(response.successResponse('data view', serializer.data), status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        exp_status = self.get_queryset_object(pk)
        response = CustomResponse()
        if not exp_status:
            return Response(response.errorResponse(404, "Data not found"), status=status.HTTP_404_NOT_FOUND)
        serializer = ExpenseStatusSerializer(exp_status, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("Data updated successfully", serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse("Validation Error", serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        exp_status = self.get_queryset_object(pk)
        response = CustomResponse()
        if not exp_status:
            return Response(response.errorResponse("Data not found"), status=status.HTTP_404_NOT_FOUND)
        exp_status.delete()
        return Response(response.errorResponse("Data deleted successfully"), status=status.HTTP_204_NO_CONTENT)