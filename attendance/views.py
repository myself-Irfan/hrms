from rest_framework import viewsets
from .models import Attendance
from .serializers import AttendanceSerializer
from rest_framework.permissions import IsAuthenticated

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'superadmin':
            return Attendance.objects.all()
        if user.role == 'employee':
            return Attendance.objects.filter(employee__user=user)
        if user.company:
            return Attendance.objects.filter(company=user.company)
        return Attendance.objects.none()

    def perform_create(self, serializer):
        if self.request.user.company:
            serializer.save(company=self.request.user.company)
        else:
            serializer.save()
