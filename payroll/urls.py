from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SalaryStructureViewSet, PayrollRecordViewSet

router = DefaultRouter()
router.register(r'structure', SalaryStructureViewSet)
router.register(r'records', PayrollRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
