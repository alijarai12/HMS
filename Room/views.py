from .models import *
from Core .utils import *
from .serializers import *
from rest_framework import status
from django.shortcuts import render
from Core .mixins import GetObjectMixin
from Restaurant .views import CustomResponse
from rest_framework.response import Response
from HMS.CustomPagination import CustomPagination
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import LimitOffsetPagination
from Core .utils import *
from Core .permissions import *
response = CustomResponse()


class RoomTypeApi(GenericAPIView):
    serializer_class = GetRoomTypeSerializer
    pagination_class = CustomPagination()
    filterset_fields = ['id', 'hotel_id']
    search_fields = ['name']

    def get(self, request):
        global response
        RoomType_obj = RoomType.objects.all()
        filter_obj = self.filter_queryset(RoomType_obj)

        paginator = self.pagination_class
        paginated_queryset = paginator.paginate_queryset(filter_obj, request)
      
        serializer = self.serializer_class(paginated_queryset, many = True)
        response_data = {
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'count':paginator.page.paginator.count,
            'data': serializer.data
        }
        if filter_obj:
            return Response(response.successResponse("data view", response_data), status=status.HTTP_200_OK)
        return Response(response.errorResponse("data not found"), status=status.HTTP_404_NOT_FOUND)
    
    
    def post(self, request):
        serializer_class = RoomTypeSerializer(data = request.data)
        # response = CustomResponse()
        global response

        if serializer_class.is_valid():
            serializer_class.save()
            response_data = {
                'data': serializer_class.data
                }
            return Response(response.successResponse('RoomType created successfully',response_data), status=status.HTTP_201_CREATED)
        else:
            return Response(response.errorResponse('Validation Error!',RoomTypeSerializer.errors), status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,pk):
        room_type = self.get_queryset_object(RoomType, pk)
        global response
        if not room_type:
            return Response(response.errorResponse('Data is not found,','Not Found'),status=status.HTTP_404_NOT_FOUND)        
        room_type.delete()
        return Response(response.errorResponse("Deleted Successfully"), status=status.HTTP_204_NO_CONTENT)
    
    def put(self,request,pk):
        room_type = self.get_queryset_object(RoomType, pk)
        global response
        if not room_type :
           return Response(response.errorResponse('Data is not found,','Not Found'),status=status.HTTP_404_NOT_FOUND)
        serializer=self.serializer_class(room_type,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("Room Type Updated Successfully", serializer.data), status=status.HTTP_200_OK)
        else:
            return Response(response.errorResponse("Validation Error!", serializer.errors), status=status.HTTP_400_BAD_REQUEST)
   




class RoomApi(GetObjectMixin, GenericAPIView, HotelFilterMixin):
    serializer_class = GetRoomSerializer
    queryset_model = Room
    pagination_class = CustomPagination()
    filterset_fields = ['id', 'room_no', 'hotel_id', 'room_type_id']
    search_fields = ['bed_count', 'capacity', 'floor_no', 'status', 'name', 'description', 'price']

    def get(self, request, pk=None):
        if pk:
            # Retrieve a single room reservation by its primary key
            try:
                room_reservation = Room.objects.get(pk=pk)
                serializer = self.serializer_class(room_reservation)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Room.DoesNotExist:
                return Response({'detail': 'Room not found.'}, status=status.HTTP_404_NOT_FOUND)

        # If no pk is provided, retrieve and paginate all room reservations
        room_reservations = self.filter_queryset(self.filter_by_hotel(Room.objects.all()))
        paginator = self.pagination_class
        paginated_queryset = paginator.paginate_queryset(room_reservations, request)
        serializer = self.serializer_class(paginated_queryset, many=True)

        response_data = {
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'count': paginator.page.paginator.count,
            'data': serializer.data
        }

        if room_reservations:
            return Response(response.successResponse("Data view", response_data), status=status.HTTP_200_OK)
        return Response(response.errorResponse('No data found'), status=status.HTTP_404_NOT_FOUND)


        
    def post(self, request):
        # global response
        serilizer = RoomSerializer(data=request.data)
        if serilizer.is_valid():
            serilizer.save()
            response_data = {
                'data':serilizer.data
                }
            return Response(response.successResponse('Room Added Sucessfully', response_data), status=status.HTTP_201_CREATED)
        else:
            return Response(response.errorResponse('Error', serilizer.errors), status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,pk):
        room = self.get_queryset_object(Room, pk)
        global response
        if not room:
           return Response(response.errorResponse('Data is not found,'),status=status.HTTP_404_NOT_FOUND)        
        room.delete()
        return Response(response.errorResponse("Deleted Successfully"), status=status.HTTP_204_NO_CONTENT)
    
    
    
    def put(self,request,pk):
        room = self.get_queryset_object(Room, pk)
        global response
        if not room :
           return Response(response.errorResponse('Data is not found,'),status=status.HTTP_404_NOT_FOUND)
        serializer=self.serializer_class(room,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("Room Updated Successfully", serializer.data), status=status.HTTP_200_OK)
        else:
            return Response(response.errorResponse("Validation Error!", serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    

class BookingApi(GetObjectMixin, GenericAPIView, HotelFilterMixin):
    serializer_class = BookingSerializer
    queryset_model = Booking
    pagination_class = CustomPagination()
    filterset_fields = ['id', 'booking_type_id', 'hotel_id', 'booking_type_id', 'room']
    search_fields = ['email', 'cancelled_reason', 'status', 'from_date', 'to_date']

    def get(self, request):
        global response
        booking_obj = Booking.objects.all()
        booking_reservation = self.filter_queryset(self.filter_by_hotel(booking_obj))

        paginator = self.pagination_class
        paginated_queryset = paginator.paginate_queryset(booking_reservation, request)
        
        serializer = GetBookingSerializer(paginated_queryset, many=True)
        response_data = {
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'count': paginator.page.paginator.count,
            'data': serializer.data
        }
        if booking_reservation:
            return Response(response.successResponse("data view", response_data), status=status.HTTP_200_OK)
        return Response(response.errorResponse('No data found'), status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request):
        global response
        serilizer = self.serializer_class(data=request.data)
        if serilizer.is_valid():
            serilizer.save()
            response_data = {'data':serilizer.data}
            return Response(response.successResponse('Booking  Sucessfully', response_data), status=status.HTTP_201_CREATED)
        else:
            return Response(response.errorResponse('Error', serilizer.errors), status=status.HTTP_400_BAD_REQUEST)
        

    def delete(self,request,pk):
        booking = self.get_queryset_object(Booking, pk)
        global response
        if not booking:
           return Response(response.errorResponse('Data is not found,','Not Found'),status=status.HTTP_404_NOT_FOUND)        
        booking.delete()
        return Response(response.errorResponse("Deleted Successfully"), status=status.HTTP_204_NO_CONTENT)
    
    def put(self,request,pk):
        booking = self.get_queryset_object(Booking, pk)
        global response
        if not booking :
           return Response(response.errorResponse('Data is not found,','Not Found'),status=status.HTTP_404_NOT_FOUND)
        serializer=self.serializer_class(booking,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("Booking Updated Successfully", serializer.data), status=status.HTTP_200_OK)
        else:
            return Response(response.errorResponse("Validation Error!", serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    

class BookingTypeApi(GenericAPIView, HotelFilterMixin):
    serializer_class = BookingTypeSerializer
    queryset_model = BookingType
    filterset_fields = ['id', 'hotel_id']
    search_fields = ['name']
    pagination_class = CustomPagination()

    def get(self,request):
        global response
       
        booking_obj = BookingType.objects.all()
        bookingType_filter = self.filter_queryset(self.filter_by_hotel(booking_obj))
        
        paginator = self.pagination_class
        paginated_queryset = paginator.paginate_queryset(bookingType_filter, request)
        
        serializer=GetBookingTypeSerializer(paginated_queryset,many=True)
        response_data = {
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'count': paginator.page.paginator.count,
            'data': serializer.data
        }
        return Response(response.successResponse('BookingType', response_data), status=status.HTTP_200_OK)
    

    def post(self, request):
        global response
        
        serilizer = self.serializer_class(data=request.data)

        if serilizer.is_valid():
            serilizer.save()
            response_data = {'data': serilizer.data}
            return Response(response.successResponse('Bookingtype created successfully',response_data), status=status.HTTP_201_CREATED)
        else:
            return Response(response.errorResponse('Validation Error!',serilizer.errors), status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,pk):
        booking_type = self.get_queryset_object(BookingType, pk)
        global response
        if not booking_type:
           return Response(response.errorResponse('Data is not found,','Not Found'),status=status.HTTP_404_NOT_FOUND)        
        booking_type.delete()
        return Response(response.errorResponse("Deleted Successfully"), status=status.HTTP_204_NO_CONTENT)
    
    def put(self,request,pk):
        booking_type = self.get_queryset_object(BookingType, pk)
        global response
        if not booking_type :
           return Response(response.errorResponse('Data is not found,','Not Found'),status=status.HTTP_404_NOT_FOUND)
        serializer=self.serializer_class(booking_type,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("Booking Type Updated Successfully", serializer.data), status=status.HTTP_200_OK)
        else:
            return Response(response.errorResponse("Validation Error!", serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    

class ServiceApi(GetObjectMixin,GenericAPIView):
    serializer_class = ServiceSerializer
    queryset_model = Service
    pagination_class = CustomPagination()
    filterset_fields = ['id', 'hotel_id']
    search_fields = ['service_name', 'service_description', 'service_description']

    def get(self, request):
        global response
        service_obj = Service.objects.all()
        service_serilizers = self.filter_queryset(service_obj)

        paginator = self.pagination_class
        paginated_queryset = paginator.paginate_queryset(service_serilizers, request)
        serializer = self.serializer_class(paginated_queryset, many=True)
        response_data = {
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'count': paginator.page.paginator.count,
            'data': serializer.data

        }
        if service_serilizers:
            return Response(response.successResponse('Service', response_data), status=status.HTTP_200_OK)
        return Response(response.errorResponse('No data found'), status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request):
        global response
        service_serilizers = self.serializer_class(data=request.data)
       
        if service_serilizers.is_valid():
            service_serilizers.save()
            response_data = {
            'data': service_serilizers.data
        }
            return Response(response.successResponse('Service Created', response_data), status=status.HTTP_201_CREATED)
        return Response(response.errorResponse("Bad Request", service_serilizers.errors), status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        method=self.get_queryset_object(BookingType, pk)
        global response
        if not method:
           return Response(response.errorResponse('Data is not found,'),status=status.HTTP_404_NOT_FOUND)        
        method.delete()
        return Response(response.errorResponse("Deleted Successfully"), status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request, pk):
        method=self.get_queryset_object(BookingType, pk)
        global response
        if not method:
           return Response(response.errorResponse('Data is not found,'),status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(method,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("Payment method Updated Successfully", serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse("Bad Request", serializer.errors), status=status.HTTP_400_BAD_REQUEST)
 

class RoomServiceApi(GetObjectMixin, GenericAPIView):
    serializer_class = RoomServiceSerializer
    pagination_class = CustomPagination()
    filterset_fields = ['id', 'service_id', 'hotel_id', 'room']
    

    def get(self, request):
        global response
        
        Roomservice_obj = RoomService.objects.all()
        Roomservice_serilizers = self.filter_queryset(Roomservice_obj)

        paginator = self.pagination_class
        paginated_queryset = paginator.paginate_queryset(Roomservice_serilizers, request)

        serializer = self.serializer_class(paginated_queryset, many=True)
    
        response_data = {
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'count': paginator.page.paginator.count,
            'data': serializer.data
        }
        
        if Roomservice_serilizers:
            return Response(response.successResponse('Service', response_data), status=status.HTTP_200_OK)
        return Response(response.errorResponse('No data found'), status=status.HTTP_404_NOT_FOUND)
 
    
    def post(self, request):
        global response
        roomservice_serilizers = self.serializer_class(data=request.data)
       
        if roomservice_serilizers.is_valid():
            
            roomservice_serilizers.save()
            response_data = {
            'data': roomservice_serilizers.data
            }
            return Response(response.successResponse('Service Created', response_data), status=status.HTTP_201_CREATED)
        return Response(response.errorResponse("Bad Request", roomservice_serilizers.errors), status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        method=self.get_queryset_object(RoomService, pk)
        global response
        if not method:
           return Response(response.errorResponse('Data is not found,'),status=status.HTTP_404_NOT_FOUND)        
        method.delete()
        return Response(response.errorResponse("Deleted Successfully"), status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request, pk):
        method=self.get_queryset_object(RoomService, pk)
        global response
        if not method:
           return Response(response.errorResponse('Data is not found,'),status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(method,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("Room service Updated Successfully", serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse("Bad Request", serializer.errors), status=status.HTTP_400_BAD_REQUEST)


class CheckInApi(GetObjectMixin, GenericAPIView):
    serializer_class = CheckInSerializer
    queryset_model = CheckIn
    pagination_class = CustomPagination()
    
    filterset_fields = ['guest_id', 'room_id', 'hotel_id']

    def get(self, request):
        global response

        checkin_obj = self.queryset_model.objects.all()
        checkin_serilozers = self.filter_queryset(checkin_obj)

        paginator = self.pagination_class
        paginated_queryset = paginator.paginate_queryset(checkin_serilozers, request)

        serializer = self.serializer_class(paginated_queryset, many=True)

        response_data = {
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'count': paginator.page.paginator.count,
            'data': serializer.data

        }
        if checkin_serilozers:
            return Response(response.successResponse('Checkin', response_data), status=status.HTTP_200_OK)
        return Response(response.errorResponse('No data found'), status=status.HTTP_404_NOT_FOUND)
    
    def post (self, request):
        global response
        checkin_serilizers = self.serializer_class(data=request.data)
        
        if checkin_serilizers.is_valid():
            checkin_serilizers.save()
            response_data = {
            'data': checkin_serilizers.data
            }
            # checkin_serilizers.save()
            return Response(response.successResponse('Checkin Created', response_data), status=status.HTTP_201_CREATED)
        return Response(response.errorResponse('Validation Error!', checkin_serilizers.errors), status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, pk):
        method=self.get_queryset_object(CheckIn, pk)
        global response
        if not method:
           return Response(response.errorResponse('Data is not found,'),status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(method,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("Checkin data Updated Successfully", serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse("Bad Request", serializer.errors), status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        Checkin_obj=self.get_queryset_object(self.queryset_model,pk)
        global response
        if not Checkin_obj:
           return Response(response.errorResponse('Data is not found,'),status=status.HTTP_404_NOT_FOUND)        
        Checkin_obj.delete()
        return Response(response.errorResponse("Deleted Successfully"), status=status.HTTP_204_NO_CONTENT)
    
class PackageApi(GetObjectMixin, GenericAPIView):
    serializer_class = PackageSerializer
    queryset_model = Package
    pagination_class = CustomPagination()
    
    filterset_fields = ['hotel_id', 'id']
    search_fields = ['name']
    

    def get(self, request):
        global response
        package_obj = self.queryset_model.objects.all()
        package_serilozers = self.filter_queryset(package_obj)

        paginator = self.pagination_class
        paginated_queryset = paginator.paginate_queryset(package_serilozers, request)

        serializer = GetPackageSerializer(paginated_queryset, many=True)

        response_data = {
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'count': paginator.page.paginator.count,
            'data': serializer.data
        }
        if package_serilozers:
            return Response(response.successResponse('package', response_data), status=status.HTTP_200_OK)
        return Response(response.errorResponse("data not found"), status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        global response
        pacage_serilizers = self.serializer_class(data=request.data)
        
        if pacage_serilizers.is_valid():
            pacage_serilizers.save()
            response_data = {
            'data': pacage_serilizers.data
            }
            
            return Response(response.successResponse('Package  Created', response_data), status=status.HTTP_201_CREATED)
        return Response(response.errorResponse('Validation Error!', pacage_serilizers.errors), status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        package_obj=self.get_queryset_object(self.queryset_model,pk)
        global response 
        if not package_obj:
           return Response(response.errorResponse('Data is not found,'),status=status.HTTP_404_NOT_FOUND)        
        package_obj.delete()
        return Response(response.errorResponse("Deleted Successfully"), status=status.HTTP_204_NO_CONTENT)


    def put(self, request, pk ):
        package_obj=self.get_queryset_object(self.queryset_model, pk)
        global response
        if not package_obj:
           return Response(response.errorResponse('Data is not found,'),status=status.HTTP_404_NOT_FOUND)
        serializer=self.serializer_class(package_obj,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("Package Updated Successfully", serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse("Validation Error!", serializer.errors), status=status.HTTP_400_BAD_REQUEST)
      

class PackageTypeApi(GetObjectMixin, GenericAPIView):
    global response
    serializer_class = PackageTypeSerializer
    pagination_class = CustomPagination()
    queryset_model = PackageType
    
    def get(self, request):       
        packagequeryset = self.queryset_model.objects.all()
        package_serilizers = self.filter_queryset(packagequeryset)
        
        paginator = self.pagination_class
        paginated_queryset = paginator.paginate_queryset(package_serilizers, request)
        
        serializer = GetPackageTypeSerializer(paginated_queryset, many=True)
        
        response_data = {
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'count': paginator.page.paginator.count,
            'data': serializer.data           
        }
        
        if serializer:
            return Response(response.successResponse('packagetype', response_data), status=status.HTTP_200_OK)
        return Response(response.errorResponse("data not found"), status=status.HTTP_404_NOT_FOUND)
    
    
    def post(self, request):        
        serilizer = self.serializer_class(data=request.data)
        if serilizer.is_valid():
            serilizer.save()
            response_data = {
            'data': serilizer.data
            }
            return Response(response.successResponse('Package Created', response_data), status=status.HTTP_201_CREATED)
        return Response(response.errorResponse('Validation Error!', serilizer.errors), status=status.HTTP_400_BAD_REQUEST)   

    def put(self, request, pk ):
        packagetype_obj=self.get_queryset_object(self.queryset_model, pk)
        
        if not packagetype_obj:
           return Response(response.errorResponse('Data is not found,'),status=status.HTTP_404_NOT_FOUND)
        serializer=self.serializer_class(packagetype_obj,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("Package Updated Successfully", serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse("Validation Error!", serializer.errors), status=status.HTTP_400_BAD_REQUEST)
        
        
    def delete(self,request, pk):
        packagetype_obj=self.get_queryset_object(self.queryset_model,pk)
        if not packagetype_obj:
           return Response(response.errorResponse('Data is not found,'),status=status.HTTP_404_NOT_FOUND)        
        packagetype_obj.delete()
        return Response(response.errorResponse("Deleted Successfully"), status=status.HTTP_204_NO_CONTENT)