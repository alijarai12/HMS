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


class OrganizationTypeList(HotelFilterMixin, GenericAPIView):
    permission_classes = [CustomModelPermission]
    queryset_model = OrganizationType
    pagination_class = CustomPagination()
    search_fields = ['org_type_name']
    filterset_fields = ['hotel_id']

    def get(self, request):
        print(request.user)
        queryset_data = OrganizationType.objects.all()
        organization_types = self.filter_queryset(self.filter_by_hotel(queryset_data))
        paginator = self.pagination_class
        paginated_queryset = paginator.paginate_queryset(organization_types, request)
        serializer = GetOrganizationTypeSerializer(paginated_queryset, many=True)
        response_data = {
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'count': paginator.page.paginator.count,
            'data': serializer.data
        }
        response = CustomResponse()
        if organization_types:
            return Response(response.successResponse("data view", response_data), status=status.HTTP_200_OK)
        else:
            return Response(response.errorResponse('No data found'), status=status.HTTP_404_NOT_FOUND)

    
    
    def post(self, request, format=None):
        serializer = OrganizationTypeSerializer(data=request.data)
        response=CustomResponse()
        
        if serializer.is_valid():
            serializer.save()
            response_data = {
            'data': serializer.data
        }

            return Response(response.successResponse('data created',response_data), status=status.HTTP_201_CREATED)
        return Response(response.errorResponse('Error Occured',serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    

class OrganizationTypeDetail(GetObjectMixin, APIView):
    permission_classes = [HotelAssociatedObj, CustomModelPermission]
    queryset_model = OrganizationType

    # def get_queryset_object(self, pk):
    #     try:
    #         return OrganizationType.objects.get(pk=pk)
    #     except OrganizationType.DoesNotExist:
    #         return None
        
    def get(self,request, pk):
        organization_type = self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not organization_type:
           return Response(response.errorResponse('Data is not found'),status=status.HTTP_404_NOT_FOUND)
        serializer=GetOrganizationTypeSerializer(organization_type)
        return Response(response.successResponse('Organization Type Details',serializer.data),status=status.HTTP_200_OK)

    def put(self, request, pk):
        organization_type=self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not organization_type:
           return Response(response.errorResponse('Data is not found'),status=status.HTTP_404_NOT_FOUND)
        serializer=OrganizationTypeSerializer(organization_type,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("Organization Type Updated Successfully", serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse("Bad Request", serializer.errors), status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, pk):
        organization_type=self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not organization_type:
           return Response(response.errorResponse('Data is not found'),status=status.HTTP_404_NOT_FOUND)        
        organization_type.delete()
        return Response(response.errorResponse(204, "Deleted Successfully"), status=status.HTTP_204_NO_CONTENT)
    


class OrganizationList(HotelFilterMixin, GenericAPIView):
    permission_classes = [CustomModelPermission]
    queryset_model = Organization
    pagination_class = CustomPagination()
    search_fields = ['organization_name']
    filterset_fields = ['hotel_id','organization_type']

    def get(self, request):
        queryset_data = Organization.objects.all()
        organizations = self.filter_queryset(self.filter_by_hotel(queryset_data))
        paginator = self.pagination_class
        paginated_queryset = paginator.paginate_queryset(organizations, request)
        serializer = GetOrganizationSerializer(paginated_queryset, many=True)
        response_data = {
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'count': paginator.page.paginator.count,
            'data': serializer.data
        }
        response = CustomResponse()
        #print(response_data)
        if organizations:
            return Response(response.successResponse("data view", response_data), status=status.HTTP_200_OK)
        else:
            return Response(response.errorResponse('No data found'), status=status.HTTP_404_NOT_FOUND)

    
    
    def post(self, request, format=None):
        serializer = OrganizationSerializer(data=request.data)
        response=CustomResponse()
        
        if serializer.is_valid():
            serializer.save()
            response_data = {
            'data': serializer.data
        }

            return Response(response.successResponse('data created',response_data), status=status.HTTP_201_CREATED)
        return Response(response.errorResponse('Error Occured',serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    


class OrganizationDetail(GetObjectMixin, APIView):
    permission_classes = [HotelAssociatedObj, CustomModelPermission]
    queryset_model = Organization
    filterset_fields = ['id', 'hote_id']
    search_fields  = ['organization_name']

    # def get_queryset_object(self, pk):
    #     try:
    #         return Organization.objects.get(pk=pk)
    #     except Organization.DoesNotExist:
    #         return None
        
    def get(self,request, pk):
        organization = self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not organization:
           return Response(response.errorResponse('Data is not found'),status=status.HTTP_404_NOT_FOUND)
        serializer=GetOrganizationSerializer(organization)
        return Response(response.successResponse('Organization Details',serializer.data),status=status.HTTP_200_OK)

    def put(self, request, pk):
        organization=self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not organization:
           return Response(response.errorResponse('Data is not found'),status=status.HTTP_404_NOT_FOUND)
        serializer=OrganizationSerializer(organization,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("Organization Updated Successfully", serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse("Bad Request", serializer.errors), status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, pk):
        organization=self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not organization:
           return Response(response.errorResponse('Data is not found'),status=status.HTTP_404_NOT_FOUND)        
        organization.delete()
        return Response(response.errorResponse("Deleted Successfully"), status=status.HTTP_204_NO_CONTENT)
    

class GuestTypeList(HotelFilterMixin, GenericAPIView):
    permission_classes = [CustomModelPermission]
    queryset_model = GuestType
    pagination_class = CustomPagination()
    search_fields = ['guest_type_name']
    filterset_fields = ['hotel_id']

    def get(self, request):
        queryset_data = GuestType.objects.all()
        guest_types = self.filter_queryset(self.filter_by_hotel(queryset_data))
        paginator = self.pagination_class
        paginated_queryset = paginator.paginate_queryset(guest_types, request)
        serializer = GetGuestTypeSerializer(paginated_queryset, many=True)
        response_data = {
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'count': paginator.page.paginator.count,
            'data': serializer.data
        }
        response = CustomResponse()
        if guest_types:
            return Response(response.successResponse("data view", response_data), status=status.HTTP_200_OK)
        else:
            return Response(response.successResponse('No data found'), status=status.HTTP_200_OK)

    
    
    def post(self, request, format=None):
        serializer = GuestTypeSerializer(data=request.data)
        response=CustomResponse()
        
        if serializer.is_valid():
            serializer.save()
            response_data = {
            'data': serializer.data
        }

            return Response(response.successResponse('data created',response_data), status=status.HTTP_201_CREATED)
        return Response(response.errorResponse('Error Occured',serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    

class GuestTypeDetail(GetObjectMixin, APIView):
    permission_classes = [HotelAssociatedObj, CustomModelPermission]
    queryset_model = GuestType
    filterset_fields = ['hotel_id', 'id']
    search_fields = ['guest_type_name']

    # def get_queryset_object(self, pk):
    #     try:
    #         return GuestType.objects.get(pk=pk)
    #     except GuestType.DoesNotExist:
    #         return None
        
    def get(self,request, pk):
        guest_type_detail = self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not guest_type_detail:
           return Response(response.errorResponse('Data is not found'),status=status.HTTP_404_NOT_FOUND)
        serializer=GetGuestTypeSerializer(guest_type_detail)
        return Response(response.successResponse('Guest Type Details',serializer.data),status=status.HTTP_200_OK)

    def put(self, request, pk):
        guest_type_detail=self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not guest_type_detail:
           return Response(response.errorResponse('Data is not found'),status=status.HTTP_404_NOT_FOUND)
        serializer=GuestTypeSerializer(guest_type_detail,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("Guest Type  Updated Successfully", serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse("Bad Request", serializer.errors), status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, pk):
        guest_type_detail=self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not guest_type_detail:
           return Response(response.errorResponse('Data is not found'),status=status.HTTP_404_NOT_FOUND)        
        guest_type_detail.delete()
        return Response(response.errorResponse("Deleted Successfully"), status=status.HTTP_204_NO_CONTENT)
    

class GuestList(HotelFilterMixin, GenericAPIView):
    permission_classes = [CustomModelPermission]
    queryset_model = Guest
    pagination_class = CustomPagination()
    search_fields = ['first_name','middle_name','last_name','address','phone']
    filterset_fields = ['hotel_id','guest_type','organization']

    def get(self, request):
        queryset_data = Guest.objects.all()
        guests = self.filter_queryset(self.filter_by_hotel(queryset_data))
        paginator = self.pagination_class
        paginated_queryset = paginator.paginate_queryset(guests, request)
        serializer = GetGuestSerializer(paginated_queryset, many=True)
        response_data = {
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'count': paginator.page.paginator.count,
            'data': serializer.data
        }
        
        response = CustomResponse()
        if guests:
            return Response(response.successResponse("data view", response_data), status=status.HTTP_200_OK)
        else:
            return Response(response.successResponse('No data found'), status=status.HTTP_200_OK)
    
    
    def post(self, request, format=None):
        serializer = GuestSerializer(data=request.data)
        response=CustomResponse()
        
        if serializer.is_valid():
            serializer.save()
            response_data = {
            'data': serializer.data
        }

            return Response(response.successResponse('data created',response_data), status=status.HTTP_201_CREATED)
        return Response(response.errorResponse('Error Occured',serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    

class GuestDetail(GetObjectMixin, APIView):
    permission_classes = [HotelAssociatedObj, CustomModelPermission]
    queryset_model = Guest
    filterset_fields = ['hotel_id', 'id']
    search_filter = ['first_name', 'middle_name', 'last_name', 'address', 'phone']

    # def get_queryset_object(self, pk):
    #     try:
    #         return Guest.objects.get(pk=pk)
    #     except Guest.DoesNotExist:
    #         return None
        
    def get(self,request, pk):
        guest_detail = self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not guest_detail:
           return Response(response.errorResponse('Data is not found'),status=status.HTTP_404_NOT_FOUND)
        serializer=GetGuestSerializer(guest_detail)
        return Response(response.successResponse('Guest Type Details',serializer.data),status=status.HTTP_200_OK)

    def put(self, request, pk):
        guest_detail=self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not guest_detail:
           return Response(response.errorResponse('Data is not found'),status=status.HTTP_404_NOT_FOUND)
        serializer=GuestSerializer(guest_detail,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("Guest Type  Updated Successfully", serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse("Bad Request", serializer.errors), status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, pk):
        Guest_detail=self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not Guest_detail:
           return Response(response.errorResponse('Data is not found'),status=status.HTTP_404_NOT_FOUND)        
        Guest_detail.delete()
        return Response(response.errorResponse("Deleted Successfully"), status=status.HTTP_204_NO_CONTENT)
 
    
class MembershipTypeList(HotelFilterMixin, GenericAPIView): 
    permission_classes = [CustomModelPermission]
    queryset_model = MembershipType
    pagination_class = CustomPagination()
    search_fields = ['name']
    filterset_fields = ['hotel_id', 'id']

    def get(self, request):
        queryset_data = MembershipType.objects.all()
        membership_type = self.filter_queryset(self.filter_by_hotel(queryset_data))
        paginator = self.pagination_class
        paginated_queryset = paginator.paginate_queryset(membership_type, request)
        serializer = MembershipTypeSerializer(paginated_queryset, many=True)
        response_data = {
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'count': paginator.page.paginator.count,
            'data': serializer.data
        }
        
        response = CustomResponse()
        if membership_type:
            return Response(response.successResponse("data view", response_data), status=status.HTTP_200_OK)
        else:
            return Response(response.errorResponse('No data found'), status=status.HTTP_404_NOT_FOUND)
    
    
    def post(self, request, format=None):
        # request.data['hotel_id'] = request.user.hotel_id.id
        serializer = MembershipTypeSerializer(data=request.data)
        response=CustomResponse()
        
        if serializer.is_valid():
            serializer.save()
            response_data = {
            'data': serializer.data
        }

            return Response(response.successResponse('data created',response_data), status=status.HTTP_201_CREATED)
        return Response(response.errorResponse('Error Occured',serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    

class MembershipTypeDetail(GetObjectMixin, APIView):
    permission_classes = [HotelAssociatedObj, CustomModelPermission]
    queryset_model = MembershipType
    filterset_fields = ['hotel_id', 'id']
    search_filter = ['name']


        
    def get(self,request, pk):
        membership_type_detail = self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not membership_type_detail:
           return Response(response.errorResponse('Data is not found'),status=status.HTTP_404_NOT_FOUND)
        serializer=MembershipTypeSerializer(membership_type_detail)
        return Response(response.successResponse('Guest Type Details',serializer.data),status=status.HTTP_200_OK)

    def put(self, request, pk):
        # request.data['hotel_id'] = request.user.hotel_id.id
        membership_type_detail=self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not membership_type_detail:
           return Response(response.errorResponse('Data is not found'),status=status.HTTP_404_NOT_FOUND)
        serializer=MembershipTypeSerializer(membership_type_detail,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("Guest Type  Updated Successfully", serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse("Bad Request", serializer.errors), status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, pk):
        membership_type_detail=self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not membership_type_detail:
           return Response(response.errorResponse('Data is not found'),status=status.HTTP_404_NOT_FOUND)        
        membership_type_detail.delete()
        return Response(response.errorResponse("Deleted Successfully"), status=status.HTTP_204_NO_CONTENT)


class MembershipList(HotelFilterMixin, GenericAPIView): 
    permission_classes = [CustomModelPermission]
    queryset_model = Membership
    pagination_class = CustomPagination()
    search_fields = ['name']
    filterset_fields = ['hotel_id','type_id']

    def get(self, request):
        queryset_data = Membership.objects.all()
        membership = self.filter_queryset(self.filter_by_hotel(queryset_data))
        paginator = self.pagination_class
        paginated_queryset = paginator.paginate_queryset(membership, request)
        serializer = GetMembershipSerializer(paginated_queryset, many=True)
        response_data = {
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'count': paginator.page.paginator.count,
            'data': serializer.data
        }
        
        response = CustomResponse()
        if membership:
            return Response(response.successResponse("data view", response_data), status=status.HTTP_200_OK)
        else:
            return Response(response.errorResponse('No data found'), status=status.HTTP_404_NOT_FOUND)

    
    
    def post(self, request, format=None):
        # request.data['hotel_id'] = request.user.hotel_id.id
        serializer = MembershipSerializer(data=request.data)
        response=CustomResponse()
        
        if serializer.is_valid():
            serializer.save()
            response_data = {
            'data': serializer.data
        }

            return Response(response.successResponse('data created',response_data), status=status.HTTP_201_CREATED)
        return Response(response.errorResponse('Error Occured',serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    

class MembershipDetail(GetObjectMixin, APIView):
    permission_classes = [HotelAssociatedObj, CustomModelPermission]
    queryset_model = Membership
    filterset_fields = ['id', 'hotel_id']
    search_fields = ['name', 'number']

    # def get_queryset_object(self, pk):
    #     try:
    #         return Membership.objects.get(pk=pk)
    #     except Membership.DoesNotExist:
    #         return None
        
    def get(self,request, pk):
        membership_detail = self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not membership_detail:
           return Response(response.errorResponse('Data is not found'),status=status.HTTP_404_NOT_FOUND)
        serializer=GetMembershipSerializer(membership_detail)
        return Response(response.successResponse('Guest Type Details',serializer.data),status=status.HTTP_200_OK)

    def put(self, request, pk):
        # request.data['hotel_id'] = request.user.hotel_id.id
        membership_detail=self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not membership_detail:
           return Response(response.errorResponse('Data is not found'),status=status.HTTP_404_NOT_FOUND)
        serializer=MembershipSerializer(membership_detail,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("Guest Type  Updated Successfully", serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse("Bad Request", serializer.errors), status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, pk):
        membership_detail=self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not membership_detail:
           return Response(response.errorResponse('Data is not found'),status=status.HTTP_404_NOT_FOUND)        
        membership_detail.delete()
        return Response(response.errorResponse("Deleted Successfully"), status=status.HTTP_204_NO_CONTENT)


class MembershipFeedbackList(HotelFilterMixin, GenericAPIView): 
    permission_classes = [CustomModelPermission]
    queryset_model = MembershipFeedback
    pagination_class = CustomPagination()
    search_fields = ['feedback']
    filterset_fields = ['hotel_id','member_id']

    def get(self, request):
        queryset_data = MembershipFeedback.objects.all()
        membership_feedback = self.filter_queryset(self.filter_by_hotel(queryset_data))
        paginator = self.pagination_class
        paginated_queryset = paginator.paginate_queryset(membership_feedback, request)
        serializer = GetMembershipFeedbackSerializer(paginated_queryset, many=True)
        response_data = {
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'count': paginator.page.paginator.count,
            'data': serializer.data
        }
        
        response = CustomResponse()
        if membership_feedback:
            return Response(response.successResponse("data view", response_data), status=status.HTTP_200_OK)
        else:
            return Response(response.errorResponse('No data found'), status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request, format=None):
        # request.data['hotel_id'] = request.user.hotel_id.id
        serializer = MembershipFeedbackSerializer(data=request.data)
        response=CustomResponse()
        
        if serializer.is_valid():
            serializer.save()
            response_data = {
            'data': serializer.data
        }

            return Response(response.successResponse('data created',response_data), status=status.HTTP_201_CREATED)
        return Response(response.errorResponse('Error Occured',serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    

class MembershipFeedbackDetail(GetObjectMixin, APIView):
    permission_classes = [HotelAssociatedObj, CustomModelPermission]
    queryset_model = MembershipFeedback
    filterset_fields = ['member_id__id', 'id', 'hotel_id']

    # def get_queryset_object(self, pk):
    #     try:
    #         return MembershipFeedback.objects.get(pk=pk)
    #     except MembershipFeedback.DoesNotExist:
    #         return None
        
    def get(self,request, pk):
        membership_feedback_detail = self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not membership_feedback_detail:
           return Response(response.errorResponse('Data is not found'),status=status.HTTP_404_NOT_FOUND)
        serializer=GetMembershipFeedbackSerializer(membership_feedback_detail)
        return Response(response.successResponse('Guest Type Details',serializer.data),status=status.HTTP_200_OK)

    def put(self, request, pk):
        # request.data['hotel_id'] = request.user.hotel_id.id
        membership_feedback_detail=self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not membership_feedback_detail:
           return Response(response.errorResponse('Data is not found'),status=status.HTTP_404_NOT_FOUND)
        serializer=MembershipFeedbackSerializer(membership_feedback_detail,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("Guest Type  Updated Successfully", serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse("Bad Request", serializer.errors), status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, pk):
        membership_feedback_detail=self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not membership_feedback_detail:
           return Response(response.errorResponse('Data is not found,','Not Found'),status=status.HTTP_404_NOT_FOUND)        
        membership_feedback_detail.delete()
        return Response(response.errorResponse("Deleted Successfully"), status=status.HTTP_204_NO_CONTENT)