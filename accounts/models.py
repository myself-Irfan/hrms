from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from hrms_project.models import BaseModel


class ClientLicenseInfo(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='license_info')
    license_count = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        db_table = 'client_license_info'