from rest_framework import viewsets
from .models import Department, Designation, Employee
from .serializers import DepartmentSerializer, DesignationSerializer, EmployeeSerializer
from rest_framework.permissions import IsAuthenticated

class BaseCompanyViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'superadmin':
            return self.queryset.all()
        if user.company:
            return self.queryset.filter(company=user.company)
        return self.queryset.none()
    
    def perform_create(self, serializer):
        if self.request.user.company:
            serializer.save(company=self.request.user.company)
        else:
            serializer.save()

class DepartmentViewSet(BaseCompanyViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class DesignationViewSet(BaseCompanyViewSet):
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer

class EmployeeViewSet(BaseCompanyViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
