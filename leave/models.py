from django.db import models
from employees.models import Employee
from tenants.models import Company

class LeaveType(models.Model):
    name = models.CharField(max_length=100)
    days_allowed = models.PositiveIntegerField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='leave_types')

    def __str__(self):
        return self.name

class LeaveRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leave_requests')
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='leave_requests')

    def __str__(self):
        return f"{self.employee} - {self.leave_type} ({self.status})"
