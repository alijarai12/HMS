from django.urls import path
from .views import *

urlpatterns = [
    path('gym/', GymApiView.as_view(), name='gym'),
    path('gym/<int:pk>/', GymApiView.as_view(), name='gym'),
    
    path('gym-packages/', GymPackageApi.as_view(), name='gympackage'),
    path('gym-packages/<int:pk>/', GymPackageApi.as_view(), name='gympackage'),
    
    path('gym-member/', GymMemberApi.as_view(), name='gymmember'),
    path('gym-member/<int:pk>/', GymMemberApi.as_view(), name='gymmember'),
    
    path('gym-feedback/', GymFeedbackApi.as_view(), name='gymfeedback'), 
    path('gym-feedback/<int:pk>/', GymFeedbackApi.as_view(), name='gymfeedback'), 
    
    path('gym-attendance/', GymAttendanceApi.as_view(), name='gymattendance'),
    path('gym-attendance/<int:pk>/', GymAttendanceApi.as_view(), name='gymattendance'),
    
    path('nutrition-plan/', NutritionPlanApi.as_view(), name='nutritionplan'),
    path('nutrition-plan/<int:pk>/', NutritionPlanApi.as_view(), name='nutrition-plan'),
    
    path('spa/', SpaApi.as_view(), name='spa'),
    path('spa/<int:pk>/', SpaApi.as_view(), name='spa'),
    
    path('spa-member/', SpaMemberApi.as_view(), name='spamember'),
    path('spa-member/<int:pk>/', SpaMemberApi.as_view(), name='spamember'),
    
    path('spa-package/', SpaPackageApiView.as_view(), name='spapackage'),
    path('spa-package/<int:pk>/', SpaPackageApiView.as_view(), name='spapackage'),
    
    path('spa-service/', SpaServiceApi.as_view(), name='spaservice'),
    path('spa-service/<int:pk>/', SpaServiceApi.as_view(), name='spaservice'),
    
    path('spa-feedback/', SpaFeedbackApi.as_view(), name='spafeedback'),
    path('spa-feedback/<int:pk>/', SpaFeedbackApi.as_view(), name='spafeedback'),
    
    path('spa-booking/', SpaBookingApiView.as_view(), name='spabooking'),
    path('spa-booking/<int:pk>/', SpaBookingApiView.as_view(), name='spabooking'),
    
    path('spa-invoice/', SpaInvoiceApi.as_view(), name='spainvoice'),
    path('spa-invoice/<int:pk>/', SpaInvoiceApi.as_view(), name='spainvoice'),
    
    path('gym-invoice/', GymInvoiceApi.as_view(), name='gyminvoice'),
    path('gym-invoice/<int:pk>/', GymInvoiceApi.as_view(), name='gyminvoice'),
    
    
]
