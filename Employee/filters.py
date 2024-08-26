import django_filters
from .models import *
from django.db import models
from rest_framework.filters import SearchFilter


# class DataFilters(django_filters.FilterSet):
#     class Meta:
#         model = EmployeePost
#         fields = ['post_name']





# def dynamic_search(self, queryset, query_params, search_fields=None):
#     """
#     Dynamically search through the queryset based on provided or default search_fields and the query parameters.
#     """
#     if search_fields is None:
#         search_fields = self.search_fields

#     search_query = query_params.get('search', '').strip()
#     if not search_query:
#         return queryset

#     queries = [models.Q(**{f"{field}__icontains": search_query}) for field in search_fields]
#     query = queries.pop()

#     for item in queries:
#         query |= item

#     return queryset.filter(query)



# def filter_and_search(self, queryset, request):
#     """
#     Apply filtering and searching on the provided queryset based on the request parameters.
#     """
#     # Check for dynamic filter fields in the request
#     dynamic_filter_fields = request.query_params.get('filter_fields')
#     if dynamic_filter_fields:
#         self.filter_fields = dynamic_filter_fields.split(',')

#     # Check for dynamic search fields in the request
#     dynamic_search_fields = request.query_params.get('search_fields')
#     if dynamic_search_fields:
#         self.search_fields = dynamic_search_fields.split(',')

#     # Apply Filtering using UniversalFilter
#     filters = UniversalFilter(data=request.query_params, queryset=queryset, filter_model=Department, fields_to_filter=self.filter_fields)
#     queryset = filters.qs

#     # Apply Searching using DRF's SearchFilter
#     for backend in list(self.filter_backends):
#         queryset = backend().filter_queryset(request, queryset, self)
    
#     return queryset


# filters_utils.py

class UniversalFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        model = kwargs.pop('filter_model', None)
        fields_to_filter = kwargs.pop('fields_to_filter', [])
        print(fields_to_filter)
        
        # Dynamically create filters based on the provided fields
        for field_name in fields_to_filter:
            self.base_filters[field_name] = django_filters.CharFilter(field_name, lookup_expr='icontains')
            
        if model:
            self._meta.model = model
            self._meta.fields = fields_to_filter
        
        super(UniversalFilter, self).__init__(*args, **kwargs)


def filter_and_search(queryset, request, filter_backends, search_fields, filter_fields, filter_model, view_instance):
    """
    Apply filtering and searching on the provided queryset based on the request parameters.
    """
    # Check for dynamic filter fields in the request
    dynamic_filter_fields = request.query_params.get('filter_fields')
    if dynamic_filter_fields:
        filter_fields = dynamic_filter_fields.split(',')

    # Check for dynamic search fields in the request
    dynamic_search_fields = request.query_params.get('search_fields')
    if dynamic_search_fields:
        search_fields = dynamic_search_fields.split(',')

    # Apply Filtering using UniversalFilter
    filters = UniversalFilter(data=request.query_params, queryset=queryset, filter_model=filter_model, fields_to_filter=filter_fields)
    queryset = filters.qs

    # Apply Searching using the given filter_backends
    for backend in filter_backends:
        queryset = backend().filter_queryset(request, queryset, view_instance)
    
    return queryset


import django_filters

class DepartmentFilter(django_filters.FilterSet):
    dept_name = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Department
        fields = ['dept_name', 'description']
