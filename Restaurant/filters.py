import django_filters
from .models import OrderItem

class OrderItemFilter(django_filters.FilterSet):
    table_no = django_filters.NumberFilter(field_name='table_id__table_no', lookup_expr='exact')
    class Meta:
        model = OrderItem
        fields = ['latest_table_token', 'table_no']