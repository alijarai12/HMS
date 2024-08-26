from rest_framework import serializers
from .models import *
from Employee.serializers import *


class GetOrganizationTypeSerializer(serializers.ModelSerializer):
    # hotel_id=HotelSerializer()

    class Meta:
        model = OrganizationType
        # fields = '__all__'
        exclude = ['hotel_id']

class OrganizationTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrganizationType
        fields = '__all__'

class GetOrganizationSerializer(serializers.ModelSerializer):
    # hotel_id=HotelSerializer()
    organization_type=OrganizationTypeSerializer()

    class Meta:
        model = Organization
        # fields = '__all__'
        exclude = ['hotel_id']

class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = '__all__'

class GetGuestTypeSerializer(serializers.ModelSerializer):
    # hotel_id=HotelSerializer()

    class Meta:
        model = GuestType
        # fields = '__all__'
        exclude = ['hotel_id']


class GuestTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = GuestType
        fields = '__all__'

class GetGuestSerializer(serializers.ModelSerializer):
    guest_type = GuestTypeSerializer()
    organization = OrganizationSerializer()
    # hotel_id = HotelSerializer()

    class Meta:
        model = Guest
        # fields = '__all__'
        exclude = ['hotel_id']

class GuestSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Guest
        fields = '__all__'
        
class MembershipTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipType
        fields = '__all__'

class GetMembershipSerializer(serializers.ModelSerializer):
    type_id = MembershipTypeSerializer()
    class Meta:
        model = Membership
        fields = '__all__'

class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = '__all__'

class GetMembershipFeedbackSerializer(serializers.ModelSerializer):
    member_id = MembershipSerializer()
    class Meta:
        model = MembershipFeedback
        fields = '__all__'
    
class MembershipFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipFeedback
        fields = '__all__'
