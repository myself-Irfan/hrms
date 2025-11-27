from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResellerViewSet, CompanyViewSet

router = DefaultRouter()
router.register(r'resellers', ResellerViewSet)
router.register(r'companies', CompanyViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
