from Restaurant.models import OrderItem, Table,Food


def complete_orders_and_free_table(order_id):
    order_item = OrderItem.objects.get(id=order_id)
    table = order_item.table_id
    table_token = order_item.latest_table_token
    
    order_items_for_table = OrderItem.objects.filter(
    table_id=table, 
    latest_table_token=table_token
    ).exclude(order_status='Cancelled').update(order_status="Completed")
    
    # for order_item in order_items_for_table:
    #     order_item.order_status = "Completed"
    #     order_item.save()
     
    table.is_occupied = False
    table.save()
        

#filter querysets by logged in user's hotel
# class HotelFilterMixin:
#     def filter_by_hotel(self, queryset):    
#         if self.request.user.is_authenticated:
#             if self.request.user.is_superuser:
#                 return queryset
#             return queryset.filter(hotel_id=self.request.user.hotel_id).order_by('-id')
#         return queryset.none()  # Return an empty queryset for unauthenticated users

    # def filter_by_hotel(self, queryset):
    #     if self.request.user.is_superuser:
    #         return queryset.all()
    #     elif self.request.user.is_authenticated:
    #         return queryset.filter(hotel_id=self.request.user.hotel_id.id)
    #     return queryset.none()

from django.apps import apps

class ForeignKeyValidationMixin:
    foreign_keys = {}
    def validate_foreign_keys(self, request):
        try:
            user_hotel = request.data['hotel_id']
        except:
            return False, 'hotel_id is required'
        for app_name, model_name in self.foreign_keys.items():
            model = apps.get_model(app_name, model_name)
            fk_id = request.data.get(model_name.lower())
            if fk_id and not model.objects.filter(id=fk_id, **{'hotel_id': user_hotel}).exists():
                return False, f"Invalid {model_name} for your hotel"
        return True, ""

