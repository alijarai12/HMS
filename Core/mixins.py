from django.shortcuts import get_object_or_404

class GetObjectMixin:
    def get_queryset_object(self, queryset_model, pk):
        return get_object_or_404(queryset_model, pk=pk)

"""
class GetTableObjectMixin:
    def get_queryset_object(self, queryset_model,table_no):
        return get_object_or_404(queryset_model, table_no=table_no)

"""  
