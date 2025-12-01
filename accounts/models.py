from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from hrms_project.models import BaseModel


class ClientLicenseInfo(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='license_info')
    total_licenses = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    used_licenses = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])

    class Meta:
        db_table = 'client_license_info'

    def available_licenses(self) -> int:
        return self.total_licenses - self.used_licenses

    def can_create_user(self) -> bool:
        return self.available_licenses() > 0