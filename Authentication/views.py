from django.shortcuts import render
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import  Token
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from Core.permissions import *
from Core.utils import *
from django.contrib.auth.hashers import make_password
from rest_framework.generics import GenericAPIView
from django.db.models import Prefetch
from HMS.CustomPagination import CustomPagination


import random
import requests
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from custom_response.response import CustomResponse
from Core.mixins import *




def userProfile(user_id):
    permission_classes = [IsSuperUser]
    user = User.objects.prefetch_related('employeeinfos').get(id=user_id)
    admin_group = user.groups.filter(name='Admin')
    if user.is_superuser:
        user_data = {'username':'superuser','email':user.email}
        return user_data
    elif admin_group.exists():
        user_data = {'id':user.id,'employeeinfos':{"employee_role": {"id": 2,"name": "Admin"},'first_name':'admin','email':user.email}}
        return user_data
    user_serializer = UserProfileSerializer(user)
    return user_serializer.data



# class CustomResponse():
#     """ This class helps to inherit responses"""
#     def successResponseToken(self,code,refresh, access, msg, data=dict()):
#         context = {
#             "status_code": code,
            
#             "message": msg,
#             "data": data,
#             "error": []
#         }
#         return context
    
#     def successResponse(self, code, msg, data=dict()):
#         context = {
#             "status_code": code,
#             "message": msg,
#             "detail": data,
#             "error": []

#         }
#         return context

#     def errorResponse(self, status_code, msg, error=dict()):
#         res = {
#             "status_code": status_code,
#             "message": msg,
#             "data": [],
#             "error": error
#         }
#         return res



class HotelList(GenericAPIView):
    """ This class lists and creates the HotelList """
    permission_classes = [IsSuperUser]
    search_fields = ['hotel_name','ceo','contact','address']
    filterset_fields = []
    pagination_class = CustomPagination()

    def get(self, request):
        hotel = self.filter_queryset(Hotel.objects.all())
        response = CustomResponse()
        if hotel:
            paginator = self.pagination_class
            paginated_queryset = paginator.paginate_queryset(hotel, request)
            serializer = HotelSerializer(paginated_queryset, many=True)
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
        serializer = HotelSerializer(data=request.data)
        response = CustomResponse()
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'data': serializer.data
            }
            return Response(response.successResponse("data created", response_data), status=status.HTTP_201_CREATED)
        return Response(response.errorResponse("HTTP_400_BAD_REQUEST", serializer.errors), status=status.HTTP_400_BAD_REQUEST)



class HotelDetail(GetObjectMixin, APIView):
    """ This class retrieves,updates and deletes the HotelDetail """
    permission_classes = [HotelObj,CustomModelPermission]
    queryset_model = Hotel

    # def get_queryset_object(self, pk):
    #     try:
    #         return Hotel.objects.get(pk=pk)
    #     except Hotel.DoesNotExist:
    #         return None
        
    def get(self,request, pk):
        hotel = self.get_queryset_object(self.queryset_model, pk)
        
        response = CustomResponse()
        if not hotel:
            return Response(response.errorResponse("Data is not found.","Not Found",), status=status.HTTP_404_NOT_FOUND)
        serializer = HotelSerializer(hotel)
    
        return Response(response.successResponse("Hotel Details", serializer.data), status=status.HTTP_200_OK)
        
        # if not Hotel:
        #     return Response(response.errorResponse(404,"Data is not found",response_data), status=status.HTTP_404_NOT_FOUND)
        # serializer = HotelSerializer(Hotel)
        # return Response(response.successResponse(200, "data view"),response_data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        hotel = self.get_queryset_object(self.queryset_model, pk)
        response = CustomResponse()

        if not hotel:
            return Response(response.errorResponse("Data is not found.","Not Found"), status=status.HTTP_404_NOT_FOUND)
        
        serializer = HotelSerializer(hotel, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("data updated successfully", serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse("Invalid data", serializer.errors), status=status.HTTP_400_BAD_REQUEST) 

    def delete(self, request, pk):
        hotel = self.get_queryset_object(self.queryset_model, pk)
        response = CustomResponse()

        if not hotel:
            return Response(response.errorResponse("Data is not found.","Not Found"), status=status.HTTP_404_NOT_FOUND)
        hotel.delete()
        return Response(response.errorResponse("Data Deleted Successfully"), status=status.HTTP_204_NO_CONTENT)



class SuperUserRegistrationView(APIView):
    permission_classes = [IsSuperUser]
    # authentication_classes = [JWTAuthentication]
    
    def get(self, request):
        group = Group.objects.get(name="Super User")
        user = User.objects.filter(groups=group)
        serializer = SuperUserRegistrationSerializer(user, many=True)
        response = CustomResponse()
        return Response(response.successResponse("Super User List", serializer.data), status=status.HTTP_200_OK)
    

    def post(self, request):
        response = CustomResponse()
        serializer = SuperUserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            group = Group.objects.get(name='Super User')
            user.groups.add(group)
            response_data = {
                'data':serializer.data
            }
            return Response(response.successResponse("Super User Created Successfully", response_data), status=status.HTTP_201_CREATED)
        else:
            return Response(response.errorResponse("Bad Request", serializer.errors), status=status.HTTP_400_BAD_REQUEST)



class SuperUserRegisterAPIIdView(GetObjectMixin, APIView):
    permission_classes = [IsSuperUser]
    queryset_model = User
    # authentication_classes = [JWTAuthentication]

    # def get_queryset_object(self, id):
    #     try:
    #         user = User.objects.get(id=id, is_superuser=True)
    #         return user
    #     except User.DoesNotExist:
    #         return None

    def get(self, request, pk):
        instance = self.get_queryset_object(self.queryset_model, pk)
        if not instance:
            response = CustomResponse()
            return Response(response.errorResponse("Not Found"), status=status.HTTP_404_NOT_FOUND)

        serializer = SuperUserRegistrationSerializer(instance)
        response = CustomResponse()
        return Response(response.successResponse("Super User Detail", serializer.data), status=status.HTTP_200_OK)

    def put(self, request, pk):
        instance = self.get_queryset_object(self.queryset_model, pk)
        if not instance:
            response = CustomResponse()
            return Response(response.errorResponse("Not Found"), status=status.HTTP_404_NOT_FOUND)
        serializer = SuperUserRegistrationSerializer(
            data=request.data, instance=instance)
        if serializer.is_valid():
            serializer.save()
            response = CustomResponse()
            return Response(response.successResponse("Super User Updated Successfully", serializer.data), status=status.HTTP_200_OK)
        else:
            response = CustomResponse()
            return Response(response.errorResponse("Bad Request", serializer.errors), status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        instance = self.get_queryset_object(self.queryset_model, pk)
        if not instance:
            response = CustomResponse()
            return Response(response.errorResponse("Not Found"), status=status.HTTP_404_NOT_FOUND)
        instance.delete()
        response = CustomResponse()
        return Response(response.successResponse("Deleted Successfully"), status=status.HTTP_204_NO_CONTENT)



class UserList(HotelFilterMixin,GenericAPIView):
    """ This class lists and creates the UserList """
    permission_classes = [CustomModelPermission]
    queryset_model = User
    search_fields = ['username']
    filterset_fields = ['hotel_id']
    pagination_class = CustomPagination()

    def get(self, request):
        users_querysets = User.objects.all()
        users = self.filter_queryset(self.filter_by_hotel(users_querysets))
        response = CustomResponse()
        if users:
            paginator = self.pagination_class
            paginated_queryset = paginator.paginate_queryset(users, request)
            serializer = StaffUserSerializer(paginated_queryset, many=True)
            response_data = {
                'next': paginator.get_next_link(),
                'previous': paginator.get_previous_link(),
                'count': paginator.page.paginator.count,
                'data': serializer.data
            }
            return Response(response.successResponse("user data view successfully", response_data), status=status.HTTP_200_OK)
        return Response(response.errorResponse('No data found'), status=status.HTTP_404_NOT_FOUND)


    
class UserDetail(GetObjectMixin, APIView):
    """ This class retrieves,updates and deletes the UserDetail """
    permission_classes = [HotelAssociatedObj,CustomModelPermission]
    queryset_model = User

    # def get_queryset_object(self, pk):
    #     try:
    #         return User.objects.get(pk=pk)
    #     except User.DoesNotExist:
    #         return None

    def get(self,request, pk):
        user = self.get_queryset_object(self.queryset_model, pk)
        
        response = CustomResponse()
        if not user:
            return Response(response.errorResponse("User Data is not found.","Not Found",), status=status.HTTP_404_NOT_FOUND)
        serializer = StaffUserSerializer(user)
        return Response(response.successResponse("User Details", serializer.data), status=status.HTTP_200_OK)
        
        # if not Hotel:
        #     return Response(response.errorResponse(404,"Data is not found",response_data), status=status.HTTP_404_NOT_FOUND)
        # serializer = HotelSerializer(Hotel)
        # return Response(response.successResponse(200, "data view"),response_data, status=status.HTTP_200_OK)


    def put(self, request, pk):
        user = self.get_queryset_object(self.queryset_model, pk)
        response = CustomResponse()

        if not user:
            return Response(response.errorResponse("User Data is not found.","Not Found"), status=status.HTTP_404_NOT_FOUND)
        
        serializer = StaffUserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("User data updated successfully", serializer.data), status=status.HTTP_200_OK)

        return Response(response.errorResponse("Invalid data", serializer.errors), status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_queryset_object(self.queryset_model, pk)
        response = CustomResponse()

        if not user:
            return Response(response.errorResponse("Data is not found","Not Found"), status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response(response.successResponse("Data Deleted Successfully"), status=status.HTTP_204_NO_CONTENT)
    


class UserLoginApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(username=email, password=password)
        if user is not None:
            token,_ = Token.objects.get_or_create(user=user)
            user_profile = userProfile(user.id)
            response = CustomResponse()
            return Response(response.successResponse("You have logged in successfully",{"token":token.key,"profile":user_profile}), status=status.HTTP_200_OK)
        else:
            response = CustomResponse()
            return Response(response.errorResponse("Email or Password is incorrect"), status=status.HTTP_400_BAD_REQUEST)



class UserLogoutApiView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        user = request
        logout(user)
        response = CustomResponse()
        return Response(response.successResponse("You have successfully Logged Out"), status=status.HTTP_200_OK)



class AdminUserView(APIView):
    permission_classes = [IsSuperUser]

    def get(self,request):
        response = CustomResponse()
        admin_user = Hotel.objects.prefetch_related(Prefetch('users', queryset=User.objects.filter(groups__name='Admin'))).all()
        serializer = AdminUserSerializer(admin_user,many=True)
        return Response(response.successResponse('Admin user list',serializer.data),status=status.HTTP_200_OK)


    def post(self,request):
        response = CustomResponse()
        email = request.data.get('email')
        phone_number = request.data.get('phone_number')
        if email == None:
            return Response(response.errorResponse('Validation error',{'email':'This field is required!'}),status= status.HTTP_400_BAD_REQUEST)
        hotel_id = request.data.get('hotel_id')
        if hotel_id == None:
            return Response(response.errorResponse('Validation error',{'hotel_id':'This field is required!'}),status= status.HTTP_400_BAD_REQUEST)
        password='password'
        hash_password=make_password(password)
        data = {'email':email,'password':hash_password,'phone_number':phone_number,'hotel_id':hotel_id}
        
        serializer = UserSerializer(data=data)
        group = Group.objects.get(name='Admin')
        if serializer.is_valid():
            user_instance = serializer.save()
            user_instance.groups.add(group)
            user_instance.save()
            return Response(response.successResponse("Admin created!",{'password':password}), status=status.HTTP_201_CREATED)
        else:
            return Response(response.errorResponse('Validation error',serializer.errors),status= status.HTTP_400_BAD_REQUEST)

class GroupAPIView(APIView):
    def get(self,requset):
        groups = Group.objects.all()
        serializer = GroupSerializer(groups,many=True)
        response = CustomResponse()
        return Response(response.successResponse("Group list!",serializer.data), status=status.HTTP_200_OK)


class CreateGroupsAndPermissionsView(APIView):
    permission_classes = [IsObjectAssociatedWithHotelUser]
    # authentication_classes = [TokenAuthentication]

    def post(self, request):
        # Create Superuser group and add necessary permissions
        superuser_group, created = Group.objects.get_or_create(
            name='Super User')
        permissions = Permission.objects.all()
        superuser_group.permissions.add(*permissions)

        # Create Admin user group and add necessary permissions
        admin_user_group, created = Group.objects.get_or_create(name='Admin')
        for permission in Permission.objects.filter(codename__in=[ 'add_logentry',
                                                                   'change_logentry',
                                                                   'add_department',
                                                                   'delete_department',
                                                                   'change_department',
                                                                   'view_department',
                                                                   'add_employeepost',
                                                                   'add_attendancedate',
                                                                   'add_salutation',
                                                                   'view_department',                                                                                                           
                                                                 
                                                                    ]):
            admin_user_group.permissions.add(permission)



        manager_user_group, created = Group.objects.get_or_create(name='Manager')
        waiter_user_group, created = Group.objects.get_or_create(name='Waiter')
        others_user_group, created = Group.objects.get_or_create(name='Others')


        response = CustomResponse()
        return Response(response.successResponse("Groups and Permissions created successfully"), status=status.HTTP_201_CREATED)
    

@api_view(["POST"])
@permission_classes((AllowAny,))
def reset_password_otp(request):
    serializer = ResetPasswordRequestSerializer(data=request.data)
    if serializer.is_valid():
        mobile_number = request.data.get('mobile_number')
        try:
            user = User.objects.get(phone_number=mobile_number)
            i = True
            a = 0
            while i:
                random_number = random.randrange(10000, 100000)
                reset_pass = ResetPasswordOtp.objects.filter(otp=random_number)
                if reset_pass.exists():
                    a += 1
                    continue
                else:
                    ResetPasswordOtp.objects.create(user=user, otp=random_number)
                    break

            r = requests.post("http://api.sparrowsms.com/v2/sms/", data={
                'token': 'WSA8OmvDWVFuAidhV1PD',
                'from': 'infoSms',
                'to': mobile_number,  # Corrected this line
                'text': 'Your OTP for reset password is in HMS is ' + str(random_number)
            })

            return Response({
                'status': r.status_code,
                'message': r.text,
                'error': r.json()
            }, status=r.status_code)

        except:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'data': 'User with this mobile number does not exist!'},
                            status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes((AllowAny,))
def reset_password_otp_verify(request):
    serializer = ResetPasswordVerifySerializer(data=request.data)
    if serializer.is_valid():
        req_otp = serializer.validated_data['otp']
        new_password = serializer.validated_data['password']

        try:
            user_otp = ResetPasswordOtp.objects.get(otp=req_otp)
            user = User.objects.get(id=user_otp.user.id)
            hash_password = make_password(new_password)
            user.password = hash_password
            user.save()
            return Response({'status': status.HTTP_200_OK, 'data': 'OTP verified, Password changed successfully.'}, status=status.HTTP_200_OK)
        except ResetPasswordOtp.DoesNotExist:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'data': 'Invalid OTP!'},
                            status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'data': 'User not found!'},
                            status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# views.py


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')

    # Check if the old password is correct
    if not check_password(old_password, user.password):
        return Response({'error': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Update the password to the new one
    user.set_password(new_password)
    user.save()

    # Update the session authentication hash to prevent automatic logout
    update_session_auth_hash(request, user)

    return Response({'message': 'Password successfully changed.'}, status=status.HTTP_200_OK)
