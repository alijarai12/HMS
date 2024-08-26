from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from HMS.CustomPagination import CustomPagination
from custom_response.response import CustomResponse 
from Core .utils import *
from Core .mixins import *
from Core.custom import get_response
from Core. permissions import *

response = CustomResponse()
# Create your views here.
class GymApiView(GenericAPIView, HotelFilterMixin, GetObjectMixin):
    pagination_class = CustomPagination()
 
    def get(self, request,pk=None):
        return get_response(request,Gym,GetGymSerializer,self.pagination_class,self.filter_queryset,self.filter_by_hotel,pk)
       
    def post(self, request):
        global response
        serializer = GymSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse( 'Gym Data Posted', serializer.data), status=status.HTTP_201_CREATED)
        return Response(response.errorResponse( "Validation Error", serializer.errorss), status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        global response
        gym_model  = self.get_queryset_object(Gym, pk)
        if not gym_model:
            return Response(response.errorResponse( "Data Not found"), status=status.HTTP_400_BAD_REQUEST)
        serializer = GymSerializer(gym_model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse( "Data Updated Sucessfully", serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse( "Data Not Found"),status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        global response
        gym_model = self.get_queryset_object(Gym, pk)
        if not gym_model:
            return Response(response.errorResponse('Data is not found,','Not Found'),status=status.HTTP_404_NOT_FOUND)   
        gym_model.delete()   
        return Response(response.errorResponse("Deleted Successfully"), status=status.HTTP_204_NO_CONTENT)
        
class GymPackageApi(GenericAPIView, HotelFilterMixin, GetObjectMixin):
    
    pagination_class = CustomPagination()
    
    def get(self, request,pk=None):
        return get_response(request,GymPackages,GetGymPackagesSerializer,self.pagination_class,self.filter_queryset,self.filter_by_hotel,pk)
    
    def post(self, request):
        global response
        serializer = GymPackageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse( "Data Created", serializer.data), status=status.HTTP_201_CREATED)
        return Response(response.errorResponse( 'Validation Error', serializer.errors),status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):  
        global response
        gym_packag = self.get_queryset_object(GymPackages, pk)
        if not gym_packag:
            return Response(response.errorResponse( 'No data Found'), status=status.HTTP_400_BAD_REQUEST)
        serializer = GymPackageSerializer(gym_packag, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse( 'Data Created', serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse( 'Validation Error', serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        global response
        gym_packag = self.get_queryset_object(GymPackages, pk)
        if not gym_packag:
            return Response(response.errorResponse( "Data Not Found",), status=status.HTTP_400_BAD_REQUEST)
        gym_packag.delete()
        return Response(response.successResponse( 'Data Deleted'),status=status.HTTP_200_OK)
    
class GymMemberApi(GenericAPIView, HotelFilterMixin, GetObjectMixin):
    
    pagination_class = CustomPagination()
    
    def get(self, request,pk=None):
        return get_response(request,GymMember,GetGymMemberSerializer,self.pagination_class,self.filter_queryset,self.filter_by_hotel,pk)

    def post(self, request):
        global response
        serializer = GymMemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse( 'Data Created', serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse( 'Validation Error',serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    
    def put (self, request, pk):
        global response
        gymmember = self.get_queryset_object(GymMember, pk)
        if not gymmember:
            return Response(response.errorResponse( 'No Data found'), status=status.HTTP_400_BAD_REQUEST)
        serializer = GymMemberSerializer(gymmember, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse( 'Data Created', serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse( 'Validation Error', serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        global response
        gym_member = self.get_queryset_object(GymMember, pk)
        if not gym_member:
            return Response(response.errorResponse( 'No data found'), status=status.HTTP_400_BAD_REQUEST) 
        gym_member.delete()
        return Response(response.successResponse( 'Data deleted'), status=status.HTTP_200_OK)
    
class GymFeedbackApi(GenericAPIView, HotelFilterMixin, GetObjectMixin):
    pagination_class = CustomPagination()
    
    def get(self, request,pk=None):
        return get_response(request,GymFeedback,GetGymFeedbackSerializer,self.pagination_class,self.filter_queryset,self.filter_by_hotel,pk)
      
    def post(self, request):
        global response
        serializer = GymFeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse( 'Data Posted Sucessfully', serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse( 'Validation Error', serializer.errors), status=status.HTTP_400_BAD_REQUEST) 
    
    def put(self, request, pk):
        global response 
        gymfeedback = self.get_queryset_object(GymFeedback, pk)
        if not gymfeedback:
            return Response(response.errorResponse( 'No Data Found'), status=status.HTTP_400_BAD_REQUEST)
        serializer = GymFeedbackSerializer(gymfeedback, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse( 'Data Created', serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse( 'Validation Error', serializer.errors), status=status.HTTP_400_BAD_REQUEST)       
            
    def delete(self, rquest, pk):
        global response
        gymfeedback = self.get_queryset_object(GymFeedback,pk)
        if not gymfeedback:
            return Response(response.errorResponse( 'Error Deleting Data'), status=status.HTTP_400_BAD_REQUEST)
        gymfeedback.delete()
        return Response(response.successResponse( 'Data Deleted'), status=status.HTTP_200_OK)    

class GymAttendanceApi(GenericAPIView, HotelFilterMixin, GetObjectMixin):
    
    pagination_class =CustomPagination()
    
    def get(self, request,pk=None):
        return get_response(request,GymAttendance,GetGymAttandanceSerializer,self.pagination_class,self.filter_queryset,self.filter_by_hotel,pk)
    
    def post(self, request):
        global response
        serializer = GymAttandanceSeriilizers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse( 'Data Posted Sucessfully', serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse( 'Validation Error', serializer.errors), status=status.HTTP_400_BAD_REQUEST) 
    
    def put(self, request, pk):
        global response 
        gymattendance = self.get_queryset_object(GymAttendance, pk)
        if not gymattendance:
            return Response(response.errorResponse( 'No Data Found'), status=status.HTTP_400_BAD_REQUEST)
        serializer = GymAttandanceSeriilizers(gymattendance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse( 'Data Created', serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse( 'Validation Error', serializer.errors), status=status.HTTP_400_BAD_REQUEST)       
            
    def delete(self, rquest, pk):
        global response
        gymattendance = self.get_queryset_object(GymAttendance,pk)
        if not gymattendance:
            return Response(response.errorResponse( 'Error Deleting Data'), status=status.HTTP_400_BAD_REQUEST)
        gymattendance.delete()
        return Response(response.successResponse( 'Data Deleted'), status=status.HTTP_200_OK)   

class NutritionPlanApi(GenericAPIView, HotelFilterMixin, GetObjectMixin):
   
    pagination_class = CustomPagination()
    
    def get(self, request,pk=None):
        return get_response(request,NutritionPlan,GetNutritionPlanSerializer,self.pagination_class,self.filter_queryset,self.filter_by_hotel,pk)  
    
    def post(self, request):
        global response
        
        serializer = NutritionPlanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse( 'data created', serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse( 'Validation Error', serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        global response
        nutrition_plan = self.get_queryset_object(NutritionPlan, pk)
        if not nutrition_plan:
            return Response(response.errorResponse( 'No data found'), status=status.HTTP_400_BAD_REQUEST)
        serializer = NutritionPlanSerializer(nutrition_plan, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse( 'Data Updated', serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse( 'Validation Error', serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        global response
        nutritionplan = self.get_queryset_object(NutritionPlan, pk)
        if not nutritionplan:
            return Response(response.errorResponse( 'No Data Found'), status=status.HTTP_200_OK)
        nutritionplan.delete()
        return Response(response.successResponse( 'Data deleted'), status=status.HTTP_200_OK)
    
# SpaView

class SpaApi(GenericAPIView, HotelFilterMixin, GetObjectMixin):
    pagination_class = CustomPagination()
    
    def get(self, request,pk=None):
        return get_response(request,Spa,GetSpaSerializer,self.pagination_class,self.filter_queryset,self.filter_by_hotel,pk)
    
    def post(self, request):
        global response
        serializer = SpaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse( 'data created', serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse( 'Validation Error', serializer.errors), status= status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        global response
        spamodel = self.get_queryset_object(Spa, pk)
        if not spamodel:
            return Response(response.errorResponse( 'No Data Found'), status=status.HTTP_400_BAD_REQUEST)
        serializer = SpaSerializer(spamodel, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse( 'Data Created', serializer.data),status=status.HTTP_200_OK)
        return Response(response.errorResponse( 'Validation Error', serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        global response
        spamodel = self.get_queryset_object(Spa, pk)
        if not spamodel:
            return Response(response.errorResponse( 'No data Found'), status=status.HTTP_400_BAD_REQUEST)
        spamodel.delete()
        return Response(response.successResponse( 'Data Deleted'), status=status.HTTP_400_BAD_REQUEST)
    

class SpaMemberApi(GenericAPIView, HotelFilterMixin, GetObjectMixin):
   
    pagination_class = CustomPagination()
    
    def get(self, request,pk=None):
        return get_response(request,SpaMember,GetSpaMemberSerializer,self.pagination_class,self.filter_queryset,self.filter_by_hotel,pk)
        
    def post(self, request):
        global response
        serializer = SpaMemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse( 'Data Created', serializer.data),status=status.HTTP_201_CREATED)
        return Response(response.errorResponse( 'Validation Error', serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        global response
        spa_member_model = self.get_queryset_object(SpaMember, pk)
        if not spa_member_model:
            return Response(response.errorResponse( 'No data found'), status=status.HTTP_400_BAD_REQUEST)
        serializer = SpaMemberSerializer(spa_member_model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse( 'Data Updated', serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse( 'Validation Error', serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        global response
        spa_member_model = self.get_queryset_object(SpaMember, pk)
        if not spa_member_model:
            return Response(response.errorResponse( 'No data found'), status=status.HTTP_200_OK)
        spa_member_model.delete()
        return Response(response.successResponse( 'Data Deleted'), status=status.HTTP_200_OK)
    
class SpaPackageApiView(GenericAPIView, HotelFilterMixin, GetObjectMixin):
    pagination_class = CustomPagination()
    
    def get(self, request,pk=None):
        return get_response(request,SpaPackage,GetSpaPackageSerializer,self.pagination_class,self.filter_queryset,self.filter_by_hotel,pk)

    def post(self, request):
        global response
        serializer = SpaPackageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse( 'Data Created', serializer.data),status=status.HTTP_201_CREATED)
        return Response(response.errorResponse( 'Validation Error', serializer.errors), status=status.HTTP_400_BAD_REQUEST)
   
    def put(self, request, pk):
        global response
        spapackagemodel = self.get_queryset_object(SpaPackage, pk)
        if not spapackagemodel:
            return Response(response.errorResponse( 'No data found'), status=status.HTTP_400_BAD_REQUEST)
        serializer = SpaMemberSerializer(spapackagemodel, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse( 'Data Updated'),status=status.HTTP_200_OK)
        return Response(response.errorResponse( 'Validation Error', serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        global response
        spapackagemodel = self.get_queryset_object(SpaPackage, pk)
        if not spapackagemodel:
            return Response(response.errorResponse( 'No Data Found'),status=status.HTTP_400_BAD_REQUEST)
        spapackagemodel.delete()
        return Response(response.successResponse( 'Data Deleted'), status=status.HTTP_200_OK)
    
class SpaServiceApi(GenericAPIView, HotelFilterMixin, GetObjectMixin):
    pagination_class = CustomPagination()
    
    def get(self, request,pk=None):
        return get_response(request,SpaService,GetSpaServiceSerializer,self.pagination_class,self.filter_queryset,self.filter_by_hotel,pk)
        
    def post(self, request):
        global response
        serializer = SpaServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse( 'Data Created', serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse( 'Validation Error', serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        global response
        servicequeryset = self.get_queryset_object(SpaService, pk)
        if not servicequeryset:
            return Response(response.errorResponse( 'No Data Found'), status=status.HTTP_400_BAD_REQUEST)
        serializer = SpaServiceSerializer(servicequeryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse( 'Data Updated', serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse( 'Validation Error', serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        global response
        spaservicemodel = self.get_queryset_object(SpaService, pk)
        if not spaservicemodel:
            return Response(response.errorResponse( 'No data found'), status=status.HTTP_400_BAD_REQUEST)
        spaservicemodel.delete()
        return Response(response.successResponse( 'Data Deleted'), status=status.HTTP_200_OK)
    
class SpaFeedbackApi(GenericAPIView, HotelFilterMixin, GetObjectMixin):
    pagination_class = CustomPagination()
    
    def get(self, request,pk=None):
        return get_response(request,SpaFeedback,GetSpaFeedbackSerializer,self.pagination_class,self.filter_queryset,self.filter_by_hotel,pk)

    def post(self, request):
        global response
        serializer = SpaFeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse( 'Data Created', serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse( 'Validation Error', serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        global response
        feedbackqueryset = self.get_queryset_object(SpaFeedback, pk)
        if not feedbackqueryset:
            return Response(response.errorResponse( 'No Data Found'), status=status.HTTP_400_BAD_REQUEST)
        serializer = SpaServiceSerializer(feedbackqueryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse( 'Data Updated', serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse( 'Validation Error', serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        global response
        spafeedbackmodel = self.get_queryset_object(SpaFeedback, pk)
        if not spafeedbackmodel:
            return Response(response.errorResponse( 'No data found'), status=status.HTTP_400_BAD_REQUEST)
        spafeedbackmodel.delete()
        return Response(response.successResponse( 'Data Deleted'), status=status.HTTP_200_OK)
    

class SpaBookingApiView(GenericAPIView, HotelFilterMixin, GetObjectMixin):
    pagination_class = CustomPagination()
    
    def get(self, request,pk=None):
        return get_response(request,SpaBooking,GetSpaBookingSerializer,self.pagination_class,self.filter_queryset,self.filter_by_hotel,pk)
    
    def post(self, request):
        global response
        serializer = SpaBookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse( 'Data Created', serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse( 'Validation Error', serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        global response
        SpaBookingqueryset = self.get_queryset_object(SpaBooking, pk)
        if not SpaBookingqueryset:
            return Response(response.errorResponse( 'No Data Found'), status=status.HTTP_400_BAD_REQUEST)
        serializer = SpaBookingSerializer(SpaBookingqueryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse( 'Data Updated', serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse( 'Validation Error', serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        global response
        spabooiking_model = self.get_queryset_object(SpaBooking, pk)
        if not spabooiking_model:
            return Response(response.errorResponse( 'No Data Found'))
        spabooiking_model.delete()
        return response(response.successResponse( 'Data Deleted'), status=status.HTTP_200_OK)
    

class GymInvoiceApi(GenericAPIView, HotelFilterMixin, GetObjectMixin):
    
    pagination_class = CustomPagination()   
    
    def get(self, request,pk=None):
        return get_response(request,GymInvoice,GetGymInvoiceSerializer,self.pagination_class,self.filter_queryset,self.filter_by_hotel,pk)

    def post(self, request):
        global response
        serializer = GymInvoiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse( 'Data Created', serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse( 'Validation Error', serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        global response
        SpaBookingqueryset = self.get_queryset_object(GymInvoice, pk)
        if not SpaBookingqueryset:
            return Response(response.errorResponse( 'No Data Found'), status=status.HTTP_400_BAD_REQUEST)
        serializer = GymInvoiceSerializer(SpaBookingqueryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse( 'Data Updated', serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse( 'Validation Error', serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        global response
        spainvoive_model = self.get_queryset_object(GymInvoice, pk)
        if not spainvoive_model:
            return Response(response.errorResponse( 'No data found'), status=status.HTTP_400_BAD_REQUEST)
        spainvoive_model.delete()
        return Response(response.successResponse( 'data deleted'), status=status.HTTP_200_OK)  
    
class SpaInvoiceApi(GenericAPIView, HotelFilterMixin, GetObjectMixin):
    
    pagination_class = CustomPagination()   
    
    def get(self, request,pk=None):
        return get_response(request,SpaInvoice,GetSpaInvoiceSerializer,self.pagination_class,self.filter_queryset,self.filter_by_hotel,pk)
        
    def post(self, request):
        global response
        serializer = SpaInvoiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse( 'Data Created', serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse( 'Validation Error', serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        global response
        Spainvoicequeryset = self.get_queryset_object(SpaInvoice, pk)
        if not Spainvoicequeryset:
            return Response(response.errorResponse( 'No Data Found'), status=status.HTTP_400_BAD_REQUEST)
        serializer = SpaInvoiceSerializer(Spainvoicequeryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse( 'Data Updated', serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse( 'Validation Error', serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        
        spainvoive_model = self.get_queryset_object(SpaInvoice, pk)
        if not spainvoive_model:
            return Response(response.errorResponse( 'No data found'), status=status.HTTP_400_BAD_REQUEST)
        spainvoive_model.delete()
        return Response(response.successResponse( 'data deleted'), status=status.HTTP_200_OK)  