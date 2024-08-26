from rest_framework import serializers
from .models import *

class GetGymSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gym
        exclude = ['hotel_id']
        
class GymSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gym
        fields ='__all__'
        
class GetGymPackagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymPackages
        exclude = ['hotel_id']

class GymPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymPackages
        fields = '__all__'
        
class GetGymMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymMember
        exclude = ['hotel_id']
        
class GymMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymMember
        fields = '__all__'
        
class GetGymFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymFeedback
        exclude = ['hotel_id']
        
class GymFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymFeedback
        fields = '__all__'
        
class GetGymAttandanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymAttendance
        exclude = ['hotel_id']
        
class GymAttandanceSeriilizers(serializers.ModelSerializer):
    class Meta:
        model = GymAttendance
        fields = '__all__'

class GetNutritionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = NutritionPlan
        fields = '__all__'
class NutritionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = NutritionPlan
        fields = '__all__'


class GetSpaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spa
        exclude = ['hotel_id']
        
class SpaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spa
        fields = '__all__'
        
class GetSpaMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpaMember
        exclude = ['hotel_id']
        
class SpaMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpaMember
        fields = '__all__'
        
class GetSpaPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpaPackage
        exclude = ['hotel_id']

class SpaPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpaPackage
        fields = '__all__'
        
class GetSpaServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpaService
        exclude = ['hotel_id']

class SpaServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpaService
        fields = '__all__'
        
class GetSpaFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpaFeedback
        exclude = ['hotel_id']

class SpaFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpaFeedback
        fields = '__all__'
        
class GetSpaBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpaBooking
        exclude = ['hotel_id']

class SpaBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpaBooking
        fields = '__all__'
        
# Invoice

class GetGymInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymInvoice
        exclude = ['hotel_id']
        
class GymInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymInvoice
        fields = '__all__'


class GetSpaInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpaInvoice
        exclude = ['hotel_id']
        
class SpaInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpaInvoice
        fields = '__all__'