import random
import string
from .models import *
from .serializers import *
from rest_framework import status
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from HMS.CustomPagination import CustomPagination
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from rest_framework.generics import GenericAPIView
from django.db import IntegrityError
from Core.permissions import *
from Core.utils import *
from django.utils import timezone
from django.shortcuts import get_object_or_404
from custom_response.response import CustomResponse
from Core.mixins import *



def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

class EmployeePostList(HotelFilterMixin, GenericAPIView):
    """ This class lists and creates the EmployeePostList """
    permission_classes = [CustomModelPermission]
    queryset_model = EmployeePost
    pagination_class = CustomPagination()
    search_fields = ['post_name']
    filterset_fields = ['hotel_id']

    def get(self, request):
        response = CustomResponse()
        initial_queryset = EmployeePost.objects.all()
        #employee_post = self.filter_by_hotel(initial_queryset)
        employee_post = self.filter_queryset(self.filter_by_hotel(initial_queryset))

        if employee_post:
            paginator = self.pagination_class
            paginated_queryset = paginator.paginate_queryset(employee_post, request)
            serializer = GetEmployeePostSerializer(paginated_queryset, many=True)
            response_data = {
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'count': paginator.page.paginator.count,
            'data': serializer.data
        }
            return Response(response.successResponse("Employee data view successfully", response_data), status=status.HTTP_200_OK)
        return Response(response.errorResponse('No data found'), status=status.HTTP_404_NOT_FOUND)


    def post(self, request):
        serializer = EmployeePostSerializer(data=request.data)
        response = CustomResponse()
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("Employee Post Added successfully", serializer.data), status=status.HTTP_201_CREATED)
        return Response(response.errorResponse("Validation Error", serializer.errors), status=status.HTTP_400_BAD_REQUEST)



class EmployeePostDetail(GenericAPIView, GetObjectMixin):
    """ This class retrieves,updates and deletes the EmployeePost """
    permission_classes = [HotelAssociatedObj, CustomModelPermission]
    queryset_model = EmployeePost
    filterset_fields = ['id', 'hotel_id']
    search_fields = ['post_name']

    # def get_queryset_object(self, pk):
    #     try:
    #         return EmployeePost.objects.get(pk=pk)
    #     except EmployeePost.DoesNotExist:
    #         return None

    def get(self,request, pk):
        employee = self.get_queryset_object(self.queryset_model, pk)
        
        response = CustomResponse()
        if not employee:
            return Response(response.errorResponse("Employee Data is not found."), status=status.HTTP_404_NOT_FOUND)
        serializer = GetEmployeePostSerializer(employee)
    
        return Response(response.successResponse("Employee Details", serializer.data), status=status.HTTP_200_OK)


    def put(self, request, pk):
        employee = self.get_queryset_object(self.queryset_model, pk)
        response = CustomResponse()

        if not employee:
            return Response(response.errorResponse("Employee Data is not found."), status=status.HTTP_404_NOT_FOUND)
        
        serializer = EmployeePostSerializer(employee, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("Employee data updated successfully", serializer.data), status=status.HTTP_200_OK)

        return Response(response.errorResponse("Invalid data", serializer.errors), status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        employee = self.get_queryset_object(self.queryset_model, pk)
        response = CustomResponse()

        if not employee:
            return Response(response.errorResponse("Data is not found."), status=status.HTTP_404_NOT_FOUND)
        employee.delete()
        return Response(response.errorResponse("Data Deleted Successfully"), status=status.HTTP_204_NO_CONTENT)
    



class EmployeeInfoList(HotelFilterMixin, GenericAPIView):
    """ This class lists and creates the EmployeeInfoList """
    permission_classes = [CustomModelPermission]
    queryset_model = EmployeeInfo
    pagination_class = CustomPagination()
    search_fields = ['first_name','middle_name','last_name','contact','pan_no','permanent_address','current_address','email','user']
    filterset_fields = ['hotel_id']

    def get(self, request):
        response = CustomResponse()
        initial_employee_info = EmployeeInfo.objects.all()
        employee_info = self.filter_queryset(self.filter_by_hotel(initial_employee_info))
        if employee_info:
            paginator = self.pagination_class
            paginated_queryset = paginator.paginate_queryset(employee_info, request)
            serializer = GetEmployeeInfoSerializer(paginated_queryset, many=True)
            response_data = {
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'count': paginator.page.paginator.count,
            'data': serializer.data
        }
            return Response(response.successResponse("EmployeeInfo data view successfully", response_data), status=status.HTTP_200_OK)
        return Response(response.errorResponse('No data found'), status=status.HTTP_404_NOT_FOUND)




    def post(self, request):
        serializer = EmployeeInfoSerializer(data=request.data)
        response = CustomResponse()
        if serializer.is_valid():
            first_name=serializer.validated_data['first_name']
            last_name=serializer.validated_data['last_name']
            email=serializer.validated_data['email']
            hotel_id=request.data.get('hotel_id')
            phone_no = request.data.get('contact')
            role=request.data.get('employee_role')

            try:
                group = Group.objects.get(id=role)
            
            except (Group.DoesNotExist, IntegrityError) as e:
                error_msg = ''
                if isinstance(e, Group.DoesNotExist):
                    error_msg = f"Group for role {role} does not exist!"
                    error_field = "Group"

                return Response(response.errorResponse('Validation Error!', {error_field: [error_msg]}), status=status.HTTP_400_BAD_REQUEST)
            # password=generate_random_password()
            password = 'password'
            hash_password=make_password(password)
            data = {'first_name':first_name,'last_name':last_name,'email':email,'password':hash_password,'phone_number':phone_no,'hotel_id':hotel_id}
            user_serializer = UserSerializer(data=data)
            if user_serializer.is_valid():
                user_instance = user_serializer.save()
                user_instance.groups.add(group.id)
                user_instance.save()
            else:
                return Response(response.errorResponse('Validation error',user_serializer.errors),status=status.HTTP_400_BAD_REQUEST)


            # Update the User instance in the EmployeeInfo model
            employee_info_instance = serializer.save(user=user_instance)

            return Response(response.successResponse("EmployeeInfo and User Added successfully", {
                    'employee_info':serializer.data,
                    'password':password
                    
                }), status=status.HTTP_201_CREATED)   

            
        return Response(response.errorResponse("Validation Error", serializer.errors), status=status.HTTP_400_BAD_REQUEST)


class EmployeeInfoDetail(GenericAPIView, GetObjectMixin):
    """ This class retrieves,updates and deletes the EmployeeInfoDetail """
    permission_classes = [HotelAssociatedObj, CustomModelPermission]
    queryset_model = EmployeeInfo
    filterset_fields = ['hotel_id', 'id']
    search_fields = ['first_name', 'middle_name', 'last_name', 'contact', 'pan_no', 'permanent_address', 'current_address']

    # def get_queryset_object(self, pk):
    #     try:
    #         return EmployeeInfo.objects.get(pk=pk)
    #     except EmployeeInfo.DoesNotExist:
    #         return None


    def get(self,request, pk):
        employee_info = self.get_queryset_object(self.queryset_model, pk)
        
        response = CustomResponse()
        if not employee_info:
            return Response(response.errorResponse("EmployeeInfo Data is not found."), status=status.HTTP_404_NOT_FOUND)
        serializer = EmployeeInfoSerializer(employee_info)
    
        return Response(response.successResponse("EmployeeInfo Details", serializer.data), status=status.HTTP_200_OK)
        

    def put(self, request, pk):
        employee_info = self.get_queryset_object(self.queryset_model, pk)
        response = CustomResponse()

        if not employee_info:
            return Response(response.errorResponse("EmployeeInfo Data is not found."), status=status.HTTP_404_NOT_FOUND)
        
        serializer = EmployeeInfoSerializer(employee_info, data=request.data)
        email = request.data.get('email')
        if serializer.is_valid():
            a = serializer.save()

            user_data = {
                'email': request.data.get('email', a.user.email),
                'first_name': request.data.get('first_name', a.user.first_name),
                'last_name': request.data.get('last_name', a.user.last_name),
                'phone_number':request.data.get('contact',a.user.phone_number)
            }

            user_serializer = UserSerializer(a.user,data=user_data,partial=True)
            # user_serializer = UserSerializer(a.user,data={'email':email},partial=True)
            if user_serializer.is_valid():
                user_instance=user_serializer.save()
            if 'employee_role' in request.data:
                new_group = Group.objects.get(id=request.data['employee_role'])
                user_instance.groups.clear()
                user_instance.groups.add(new_group)
            else:
                return Response(response.errorResponse("Validation error",user_serializer.errors), status=status.HTTP_400_BAD_REQUEST)
            return Response(response.successResponse("EmployeeInfo data updated successfully", serializer.data), status=status.HTTP_200_OK)

        return Response(response.errorResponse("Invalid data", serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, pk):
        employee_info = self.get_queryset_object(self.queryset_model, pk)
        response = CustomResponse()

        if not employee_info:
            return Response(response.errorResponse("Data is not found."), status=status.HTTP_404_NOT_FOUND)
        employee_info.user.delete()
        return Response(response.errorResponse("Data Deleted Successfully"), status=status.HTTP_204_NO_CONTENT)
    

class DepartmentList(HotelFilterMixin,GenericAPIView):
    """ This class lists and creates the DepartmentDetail """
    permission_classes = [CustomModelPermission]
    queryset_model = Department
    pagination_class = CustomPagination()
    search_fields = ['dept_name', 'description']
    filterset_fields = ['manager_name']

    def get(self, request): 
        response = CustomResponse()
        initial_queryset = Department.objects.all()
        department = self.filter_queryset(self.filter_by_hotel(initial_queryset))
        if department:
            paginator = self.pagination_class
            paginated_queryset = paginator.paginate_queryset(department, request)
            serializer = DepartmentSerializer(paginated_queryset, many=True)
            response_data = {
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'count': paginator.page.paginator.count,
            'data': serializer.data
        }
            return Response(response.successResponse("Department data view successfully", response_data), status=status.HTTP_200_OK)
        return Response(response.errorResponse('No data found'), status=status.HTTP_404_NOT_FOUND)



    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)
        response = CustomResponse()
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("Department Added successfully", serializer.data), status=status.HTTP_201_CREATED)
        return Response(response.errorResponse("Validation Error", serializer.errors), status=status.HTTP_400_BAD_REQUEST)

  


class DepartmentDetail(GetObjectMixin, APIView):
    """ This class retrieves,updates and deletes the DepartmentDetail """
    permission_classes = [HotelAssociatedObj, CustomModelPermission]
    queryset_model = Department
    filterset_fields = ['hotel_id', 'id']
    search_fields = ['dept_name']

    # def get_queryset_object(self, pk):
    #     try:
    #         return Department.objects.get(pk=pk)
    #     except Department.DoesNotExist:
    #         return None


    def get(self,request, pk):
        department = self.get_queryset_object(self.queryset_model,pk)
        
        response = CustomResponse()
        if not department:
            return Response(response.errorResponse("Gender Data is not found."), status=status.HTTP_404_NOT_FOUND)
        
        serializer = DepartmentSerializer(department)
        return Response(response.successResponse("Gender Details", serializer.data), status=status.HTTP_200_OK)
        

    def put(self, request, pk):
        department = self.get_queryset_object(self.queryset_model,pk)
        response = CustomResponse()

        if not department:
            return Response(response.errorResponse("Gender Data is not found."), status=status.HTTP_404_NOT_FOUND)
        
        serializer = DepartmentSerializer(department, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("Department data updated successfully", serializer.data), status=status.HTTP_200_OK)

        return Response(response.errorResponse("Invalid data", serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, pk):
        department = self.get_queryset_object(self.queryset_model,pk)
        response = CustomResponse()

        if not department:
            return Response(response.errorResponse("Data is not found."), status=status.HTTP_404_NOT_FOUND)
        department.delete()
        return Response(response.errorResponse("Data Deleted Successfully"), status=status.HTTP_204_NO_CONTENT)
    


class AttendanceDateList(HotelFilterMixin, GenericAPIView):
    """ This class lists and creates the AttendanceDateDetail """
    permission_classes = [CustomModelPermission]
    queryset_model = AttendanceDate
    pagination_class = CustomPagination()
    search_fields = ['date']
    filterset_fields = ['hotel_id']

    def get(self, request):
        response = CustomResponse()
        # search_query = request.GET.get('search')
        initial_attendance_date = AttendanceDate.objects.all()
        # attendance_date = self.filter_by_hotel(initial_attendance_date)
        attendance_date = self.filter_queryset(self.filter_by_hotel(initial_attendance_date))
        # if search_query:
        #     attendance_date=attendance_date.filter(date__icontains=search_query)

        if attendance_date:
            paginator = self.pagination_class
            paginated_queryset = paginator.paginate_queryset(attendance_date, request)
            serializer = GetAttendanceDateSerializer(paginated_queryset, many=True)
            response_data = {
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'count': paginator.page.paginator.count,
            'data': serializer.data
        }
            return Response(response.successResponse("AttendanceDate data view successfully", response_data), status=status.HTTP_200_OK)
        return Response(response.errorResponse('No data found'), status=status.HTTP_404_NOT_FOUND)
        # return Response(response.errorResponse(404,"0 results found.","Not Found",), status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = AttendanceDateSerializer(data=request.data)
        response = CustomResponse()
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("AttendanceDate Added successfully", serializer.data), status=status.HTTP_201_CREATED)
        return Response(response.errorResponse("Validation Error", serializer.errors), status=status.HTTP_400_BAD_REQUEST)



class AttendanceDateDetail(GetObjectMixin, APIView):
    """ This class retrieves,updates and deletes the AttendanceDateDetail """
    permission_classes = [HotelAssociatedObj, CustomModelPermission]
    queryset_model = AttendanceDate
    filterset_fields = ['id', 'hotel_id']

    # def get_queryset_object(self, pk):
    #     try:
    #         return AttendanceDate.objects.get(pk=pk)
    #     except AttendanceDate.DoesNotExist:
    #         return None

    def get(self,request, pk):
        attendance_date = self.get_queryset_object(self.queryset_model, pk)
        
        response = CustomResponse()
        if not attendance_date:
            return Response(response.errorResponse("AttendanceDate Data is not found."), status=status.HTTP_404_NOT_FOUND)
        serializer = AttendanceDateSerializer(attendance_date)
    
        return Response(response.successResponse("AttendanceDate Details", serializer.data), status=status.HTTP_200_OK)
        

    def put(self, request, pk):
        attendance_date = self.get_queryset_object(self.queryset_model, pk)
        response = CustomResponse()

        if not attendance_date:
            return Response(response.errorResponse("AttendanceDate Data is not found."), status=status.HTTP_404_NOT_FOUND)
        
        serializer = AttendanceDateSerializer(attendance_date, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("AttendanceDate data updated successfully", serializer.data), status=status.HTTP_200_OK)

        return Response(response.errorResponse("Invalid data", serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, pk):
        attendance_date = self.get_queryset_object(self.queryset_model, pk)
        response = CustomResponse()

        if not attendance_date:
            return Response(response.errorResponse("Data is not found."), status=status.HTTP_404_NOT_FOUND)
        attendance_date.delete()
        return Response(response.errorResponse("Data Deleted Successfully"), status=status.HTTP_204_NO_CONTENT)



class AttendanceList(HotelFilterMixin, GenericAPIView):
    """ This class lists and creates the Attendance Detail """
    permission_classes = [CustomModelPermission]
    queryset_model = Attendance
    pagination_class = CustomPagination()
    search_fields = ['check_in_time','check_out_time','present']
    filterset_fields = ['employee','hotel_id','attendance_date']

    def get(self, request): 
        
        response = CustomResponse()
        initial_attendance = Attendance.objects.all()
        # attendance = self.filter_by_hotel(initial_attendance)
        attendance = self.filter_queryset(self.filter_by_hotel(initial_attendance))
        # search_query = request.GET.get('search')
        # if search_query:
        #     attendance=attendance.filter(employee__icontains=search_query)

        if attendance:
            paginator = self.pagination_class
            paginated_queryset = paginator.paginate_queryset(attendance, request)
            serializer = GetAttendanceSerializer(paginated_queryset, many=True)
            response_data = {
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'count': paginator.page.paginator.count,
            'data': serializer.data
        }
            return Response(response.successResponse("Attendance data view successfully", response_data), status=status.HTTP_200_OK) 
        return Response(response.errorResponse('No data found'), status=status.HTTP_404_NOT_FOUND)



    def post(self, request):
        employee_id = request.data.get('employee_id')
        hotel_id = request.data.get('hotel_id')
        present = request.data.get('present')
        

        employee = get_object_or_404(EmployeeInfo, pk=employee_id)
        hotel = get_object_or_404(Hotel, pk=hotel_id)
        
        today = timezone.now().date()
        
        # Check if the employee has already checked in for today
        existing_attendance = Attendance.objects.filter(
            employee=employee,
            attendance_date__date=today,
            hotel_id=hotel
        )
        
        if existing_attendance.exists():
            return Response({"error": "Employee has already checked in for today."}, status=status.HTTP_400_BAD_REQUEST)
        
        attendance_date, _ = AttendanceDate.objects.get_or_create(date=today, hotel_id=hotel)
        
        attendance = Attendance.objects.create(
            employee=employee,
            attendance_date=attendance_date,
            hotel_id=hotel,
            present=present
        )
        
        response = CustomResponse()
        serializer = AttendanceSerializer(attendance)
        return Response(response.successResponse("Attendance data created successfully", serializer.data), status=status.HTTP_201_CREATED)


class AttendanceDetail(GetObjectMixin, APIView):
    """ This class retrieves,updates and deletes the Attendance List Detail """
    permission_classes = [HotelAssociatedObj, CustomModelPermission]
    queryset_model = Attendance
    filterset_fields = ['id', 'hotel_id']
    search_fields = ['present']

    # def get_queryset_object(self, pk):
    #     try:
    #         return Attendance.objects.get(pk=pk)
    #     except Attendance.DoesNotExist:
    #         return None


    def get(self,request, pk):
        attendance = self.get_queryset_object(self.queryset_model, pk)
        
        response = CustomResponse()
        if not attendance:
            return Response(response.errorResponse("Attendance Data is not found."), status=status.HTTP_404_NOT_FOUND)
        serializer = AttendanceSerializer(attendance)
    
        return Response(response.successResponse("Attendance Details", serializer.data), status=status.HTTP_200_OK)
        

    def put(self, request, pk):
        attendance = self.get_queryset_object(self.queryset_model,pk)
        response = CustomResponse()

        if not attendance:
            return Response(response.errorResponse("Attendance Data is not found."), status=status.HTTP_404_NOT_FOUND)
        
        serializer = AttendanceSerializer(attendance, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("Attendance data updated successfully", serializer.data), status=status.HTTP_200_OK)

        return Response(response.errorResponse("Invalid data", serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, pk):
        attendance = self.get_queryset_object(pk)
        response = CustomResponse()

        if not attendance:
            return Response(response.errorResponse("Data is not found."), status=status.HTTP_404_NOT_FOUND)
        attendance.delete()
        return Response(response.errorResponse("Data Deleted Successfully"), status=status.HTTP_204_NO_CONTENT)
  

class ShiftList(HotelFilterMixin, GenericAPIView):
    """ This class lists and creates the ShiftDetail """
    permission_classes = [CustomModelPermission]
    queryset_model = Shift
    pagination_class = CustomPagination()
    search_fields = ['shift_name']
    filterset_fields = ['hotel_id']


    def get(self, request):
        # search_query = request.GET.get('search')
        # if search_query:
        #     shift=shift.filter(shift_name__icontains=search_query)        
        response = CustomResponse()
        shift = Shift.objects.all()
        shift = self.filter_queryset(self.filter_by_hotel(shift))

        if shift:
            paginator = self.pagination_class
            paginated_queryset = paginator.paginate_queryset(shift, request)
            serializer = GetShiftSerializer(paginated_queryset, many=True)
            response_data = {
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'count': paginator.page.paginator.count,
            'data': serializer.data
        }
            return Response(response.successResponse("Shift data view successfully", response_data), status=status.HTTP_200_OK)
        return Response(response.errorResponse('No data found'), status=status.HTTP_404_NOT_FOUND)


    def post(self, request):
        serializer = ShiftSerializer(data=request.data)
        response = CustomResponse()
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("Shift Added successfully", serializer.data), status=status.HTTP_201_CREATED)
        return Response(response.errorResponse("Validation Error", serializer.errors), status=status.HTTP_400_BAD_REQUEST)



class ShiftDetail(GetObjectMixin, APIView):
    """ This class retrieves,updates and deletes the ShiftDetail """
    permission_classes = [HotelAssociatedObj, CustomModelPermission]
    queryset_model = Shift
    filterset_fields = ['id', 'hotel_id']
    search_fields = ['name']

    # def get_queryset_object(self, pk):
    #     try:
    #         return Shift.objects.get(pk=pk)
    #     except Shift.DoesNotExist:
    #         return None


    def get(self,request, pk):
        shift = self.get_queryset_object(self.queryset_model, pk)
        
        response = CustomResponse()
        if not shift:
            return Response(response.errorResponse("Shift Data is not found."), status=status.HTTP_404_NOT_FOUND)
        serializer = GetShiftSerializer(shift)
    
        return Response(response.successResponse("Shift Details", serializer.data), status=status.HTTP_200_OK)
        

    def put(self, request, pk):
        shift = self.get_queryset_object(self.queryset_model, pk)
        response = CustomResponse()

        if not shift:
            return Response(response.errorResponse(404,"Shift Data is not found.","Not Found"), status=status.HTTP_404_NOT_FOUND)
        
        serializer = ShiftSerializer(shift, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("Shift data updated successfully", serializer.data), status=status.HTTP_200_OK)

        return Response(response.errorResponse("Invalid data", serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    


    def delete(self, request, pk):
        shift = self.get_queryset_object(self.queryset_model, pk)
        response = CustomResponse()

        if not shift:
            return Response(response.errorResponse("Data is not found."), status=status.HTTP_404_NOT_FOUND)
        shift.delete()
        return Response(response.errorResponse("Data Deleted Successfully"), status=status.HTTP_204_NO_CONTENT)
    



class EmployeeShiftList(HotelFilterMixin, GenericAPIView):
    """ This class lists and creates the EmployeeShift Detail """
    permission_classes = [CustomModelPermission]
    queryset_model = EmployeeShift
    pagination_class = CustomPagination()
    search_fields = ['date']
    filterset_fields = ['shift_name','hotel_id','employee']

    def get(self, request): 
        employeeshift = EmployeeShift.objects.all()
        employeeshift = self.filter_queryset(self.filter_by_hotel(employeeshift))
        # search_query = request.GET.get('search')
        # if search_query:
        #     employeeshift=employeeshift.filter(employee__icontains=search_query)

        response = CustomResponse()
        if employeeshift:
            paginator = self.pagination_class
            paginated_queryset = paginator.paginate_queryset(employeeshift, request)
            serializer = GetEmployeeShiftSerializer(paginated_queryset, many=True)
            response_data = {
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'count': paginator.page.paginator.count,
            'data': serializer.data            
            }
            return Response(response.successResponse("EmployeeShift data view successfully", response_data), status=status.HTTP_200_OK)
        return Response(response.errorResponse('No data found'), status=status.HTTP_404_NOT_FOUND)


    def post(self, request):
        serializer = EmployeeShiftSerializer(data=request.data)
        response = CustomResponse()
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("EmployeeShift Added successfully", serializer.data), status=status.HTTP_201_CREATED)
        return Response(response.errorResponse("Validation Error", serializer.errors), status=status.HTTP_400_BAD_REQUEST)



class EmployeeShiftDetail(GenericAPIView, APIView):
    """ This class retrieves,updates and deletes the EmployeeShift List Detail """
    permission_classes = [HotelAssociatedObj, CustomModelPermission]
    queryset_model = EmployeeShift
    search_fields = ['id', 'hotel_id']

    # def get_queryset_object(self, pk):
    #     try:
    #         return EmployeeShift.objects.get(pk=pk)
    #     except EmployeeShift.DoesNotExist:
    #         return None



    def get(self,request, pk):
        employeeshift = self.get_queryset_object(self.queryset_model, pk)
        
        response = CustomResponse()
        if not employeeshift:
            return Response(response.errorResponse("EmployeeShift Data is not found."), status=status.HTTP_404_NOT_FOUND)
        serializer = EmployeeShiftSerializer(employeeshift)
    
        return Response(response.successResponse("EmployeeShift Details", serializer.data), status=status.HTTP_200_OK)
        

    def put(self, request, pk):
        employeeshift = self.get_queryset_object(self.queryset_model, pk)
        response = CustomResponse()

        if not employeeshift:
            return Response(response.errorResponse("EmployeeShift Data is not found."), status=status.HTTP_404_NOT_FOUND)
        
        serializer = EmployeeShiftSerializer(employeeshift, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("EmployeeShift data updated successfully", serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse("Invalid data", serializer.errors), status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        employeeshift = self.get_queryset_object(self.queryset_model, pk)
        response = CustomResponse()

        if not employeeshift:
            return Response(response.errorResponse("Data is not found."), status=status.HTTP_404_NOT_FOUND)
        employeeshift.delete()
        return Response(response.errorResponse("Data Deleted Successfully"), status=status.HTTP_204_NO_CONTENT)
  
  

