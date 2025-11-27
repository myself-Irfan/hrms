from rest_framework import viewsets
from .models import Notice
from .serializers import NoticeSerializer
from employees.views import BaseCompanyViewSet
from django.db.models import Q

class NoticeViewSet(BaseCompanyViewSet):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'superadmin':
            return Notice.objects.all()
        if user.role == 'employee':
            # Notices for company AND (no specific dept OR user's dept)
            return Notice.objects.filter(
                company=user.company
            ).filter(
                Q(department__isnull=True) | Q(department=user.employee_profile.department)
            )
        if user.company:
            return Notice.objects.filter(company=user.company)
        return Notice.objects.none()
