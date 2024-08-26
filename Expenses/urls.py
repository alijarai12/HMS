from django.urls import path
from .views import *


urlpatterns = [
    path('expense/', ExpenseListView.as_view(), name='expenses'),
    path('expense/<int:pk>/', ExpenseDetailsView.as_view(), name='expensedetails'),
    path('expensestatus/', ExpenseStatusListView.as_view(), name='expensestatus'),
    path('expensestatus/<int:pk>/', ExpenseStatusDetailView.as_view(), name='expensestatusdetails'),

]