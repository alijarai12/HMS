from rest_framework.authentication import TokenAuthentication

class HotelIdTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        user_auth_tuple = super().authenticate(request)
        if user_auth_tuple:
            user, auth = user_auth_tuple
            # if not user.is_superuser:
            request._full_data = request.data.copy()
            request._full_data['hotel_id'] = user.hotel_id.id
        return user_auth_tuple
