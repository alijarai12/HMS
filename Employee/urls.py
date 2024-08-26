from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [

    path('shift/', ShiftList.as_view()),
    path('employee/', EmployeePostList.as_view()),
    path('attendance/', AttendanceList.as_view()),
    path('department/', DepartmentList.as_view()),
    path('shift/<int:pk>/', ShiftDetail.as_view()),
    path('employeeinfo/', EmployeeInfoList.as_view()),
    path('employeeshift/', EmployeeShiftList.as_view()),
    path('attendance_date/', AttendanceDateList.as_view()),
    path('attendance/<int:pk>/', AttendanceDetail.as_view()),
    path('department/<int:pk>/', DepartmentDetail.as_view()),
    path('employee/<int:pk>/', EmployeePostDetail.as_view()),
    path('employeeinfo/<int:pk>/', EmployeeInfoDetail.as_view()),
    path('employeeshift/<int:pk>/', EmployeeShiftDetail.as_view()),
    path('attendance_date/<int:pk>/', AttendanceDateDetail.as_view()),

    # path('shift/', ShiftList.as_view()),
    # path('shift/<int:pk>/', ShiftDetail.as_view()),
    # path('attendance/', AttendanceList.as_view()),
    # path('employeeshift/', EmployeeShiftList.as_view()),
    # path('attendance/<int:pk>/', AttendanceDetail.as_view()),
    # path('employeeshift/<int:pk>/', EmployeeShiftDetail.as_view()),
    # path('attendance_date/<int:pk>/', AttendanceDateDetail.as_view()),
    
    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
