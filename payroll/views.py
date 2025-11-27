from rest_framework import viewsets
from .models import SalaryStructure, PayrollRecord
from .serializers import SalaryStructureSerializer, PayrollRecordSerializer
from employees.views import BaseCompanyViewSet

class SalaryStructureViewSet(BaseCompanyViewSet):
    queryset = SalaryStructure.objects.all()
    serializer_class = SalaryStructureSerializer

class PayrollRecordViewSet(BaseCompanyViewSet):
    queryset = PayrollRecord.objects.all()
    serializer_class = PayrollRecordSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'superadmin':
            return PayrollRecord.objects.all()
        if user.role == 'employee':
            return PayrollRecord.objects.filter(employee__user=user)
        if user.company:
            return PayrollRecord.objects.filter(company=user.company)
        return PayrollRecord.objects.none()
