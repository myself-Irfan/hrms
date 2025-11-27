from rest_framework import viewsets
from .models import LeaveType, LeaveRequest
from .serializers import LeaveTypeSerializer, LeaveRequestSerializer
from rest_framework.permissions import IsAuthenticated
from employees.views import BaseCompanyViewSet

class LeaveTypeViewSet(BaseCompanyViewSet):
    queryset = LeaveType.objects.all()
    serializer_class = LeaveTypeSerializer

class LeaveRequestViewSet(BaseCompanyViewSet):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'superadmin':
            return LeaveRequest.objects.all()
        if user.role == 'employee':
            return LeaveRequest.objects.filter(employee__user=user)
        if user.company:
            return LeaveRequest.objects.filter(company=user.company)
        return LeaveRequest.objects.none()
