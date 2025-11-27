from rest_framework import viewsets
from .models import Reseller, Company
from .serializers import ResellerSerializer, CompanySerializer
from rest_framework.permissions import IsAuthenticated

class ResellerViewSet(viewsets.ModelViewSet):
    queryset = Reseller.objects.all()
    serializer_class = ResellerSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'superadmin':
            return Reseller.objects.all()
        if user.role == 'reseller':
            return Reseller.objects.filter(user=user)
        return Reseller.objects.none()

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'superadmin':
            return Company.objects.all()
        if user.role == 'reseller':
            return Company.objects.filter(reseller__user=user)
        if user.role == 'company_admin':
            return Company.objects.filter(id=user.company.id)
        return Company.objects.none()
        
    def perform_create(self, serializer):
        if self.request.user.role == 'reseller':
            serializer.save(reseller=self.request.user.reseller_profile)
        else:
            serializer.save()
