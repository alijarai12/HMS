from django.db import models
from Employee.models import Department, EmployeeInfo
from Authentication.models import Hotel

class Expense(models.Model):
    expense_name = models.CharField(max_length=200)
    expense_desc = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='expenses')
    amount = models.BigIntegerField()
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='expenses')
    expense_date = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.expense_name} - {self.id}'
    

class ExpenseStatus(models.Model):
    status = (('Approved', 'Approved'),('Pending', 'Pending'))
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='expense_status')
    status = models.CharField(choices=status, default='Pending', max_length=200)
    accepted_by = models.ForeignKey(EmployeeInfo, on_delete=models.CASCADE, related_name='expense_status')
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='expense_status')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.expense.expense_name} - {self.status}'