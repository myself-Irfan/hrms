from rest_framework import serializers
from .models import SalaryStructure, PayrollRecord

class SalaryStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryStructure
        fields = '__all__'

class PayrollRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayrollRecord
        fields = '__all__'
