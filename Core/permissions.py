from rest_framework import permissions
from rest_framework.permissions import  SAFE_METHODS


class CustomModelPermission(permissions.BasePermission):
    
    # Mapping of HTTP methods to permission codenames.
    METHOD_PERMISSIONS = {
        'GET': 'view',
        'POST': 'add',
        'PUT': 'change',
        'PATCH': 'change',
        'DELETE': 'delete'
    }

    def has_permission(self, request, view):
        queryset = view.queryset_model.objects.all()
        # check all permissions for user
        # user = request.user
        # all_permissions = user.get_all_permissions()
        # for perm in all_permissions:
        #     print(perm)

        # Get the type of permission we should be checking based on the HTTP method
        perm_type = self.METHOD_PERMISSIONS.get(request.method, None)
        if not perm_type:
            return False

        # Construct the full permission string
        # app_label = view.queryset.model._meta.app_label
        # model_name = view.queryset.model._meta.model_name
        app_label = queryset.model._meta.app_label
        model_name = queryset.model._meta.model_name
        full_perm = f"{app_label}.{perm_type}_{model_name}"
        # print('************************')
        # print(full_perm)

        # Check if the user has the required permission
        return request.user.has_perm(full_perm)



class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)



class IsObjectAssociatedWithHotelUser(permissions.BasePermission):
    hotel_field_name = 'hotel_id'
    def has_permission(self, request, view):
        # if not request.user or not request.user.is_authenticated:
        #     return False
        
        if request.user.is_superuser:
            return True
        # if not hasattr(request.user, 'hotel_id'):
        #     return False
        # Check if the view has model
        if not hasattr(view, 'queryset_model'):
            return False

        obj_id = view.kwargs.get('pk')
        if not obj_id:
            return False

        try:
            obj = view.queryset_model.objects.get(pk=obj_id)
            obj_hotel_id = getattr(obj, self.hotel_field_name)
            return obj_hotel_id == request.user.hotel_id
        except view.queryset_model.DoesNotExist:
            return False
        

#filter querysets by logged in user's hotel
class HotelFilterMixin:
    def filter_by_hotel(self, queryset):
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser:
                return queryset
            print(self.request.user.hotel_id)
            return queryset.filter(hotel_id=self.request.user.hotel_id).order_by('-id')
        return queryset.none()  # Return an empty queryset for unauthenticated users
    
    
# inject hotel_id to request data before hitting views
class HotelIdMixin:
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        if request.user.is_authenticated:
            request._full_data = request.data.copy()
            request._full_data['hotel_id'] = request.user.hotel_id.id
        # super().initial(request, *args, **kwargs)



class HotelAssociatedObj(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        if not hasattr(view, 'queryset_model'):
            return False
        obj_id = view.kwargs.get('pk')
        if not obj_id:
            return False

        try:
            obj = view.queryset_model.objects.get(pk=obj_id)
            obj_hotel_id = getattr(obj, 'hotel_id')
            return obj_hotel_id == request.user.hotel_id
        except view.queryset_model.DoesNotExist:
            return False

    

class HotelObj(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True

        return request.user.hotel_id.id == view.kwargs.get('pk')
    

class AdminUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return any(group.name == 'Admin' for group in request.user.groups.all())


class CanCreateTableReservation(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow users with a specific permission to use POST
        if request.method == 'POST' and request.user.has_perm('Restaurant.tablereservation'):
            return True
        # Allow other HTTP methods for everyone
        elif request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return False



class CanViewUnauthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True  # Allow unauthenticated users to view (GET)
        return request.user and request.user.is_authenticated  # Require authentication for other methods
