from rest_framework import serializers
from .models import Reseller, Company

class ResellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reseller
        fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
