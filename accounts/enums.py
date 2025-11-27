from django.db import models

class UserGroup(models.TextChoices):
    SUPER_ADMIN = 'SuperAdmin', 'Super Admin'
    RESELLER_ADMIN = 'ResellerAdmin', 'Reseller Admin'
    CLIENT_ADMIN = 'ClientAdmin', 'Client Admin'
    BASE_USER = 'BaseUser', 'Base User'
