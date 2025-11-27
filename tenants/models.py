from django.db import models
from django.conf import settings

class Reseller(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reseller_profile')
    max_companies = models.PositiveIntegerField(default=5)

    def __str__(self):
        return self.user.username

class Company(models.Model):
    name = models.CharField(max_length=255)
    domain = models.CharField(max_length=255, unique=True)
    address = models.TextField(blank=True)
    reseller = models.ForeignKey(Reseller, on_delete=models.SET_NULL, null=True, related_name='companies')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
