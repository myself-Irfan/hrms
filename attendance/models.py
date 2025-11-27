from django.db import models
from employees.models import Employee
from tenants.models import Company

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendances')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    clock_in = models.TimeField()
    clock_out = models.TimeField(null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return f"{self.employee} - {self.date}"
