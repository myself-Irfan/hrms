from django.db import models
from tenants.models import Company
from employees.models import Department

class Notice(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='notices')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, help_text="Leave blank for all departments")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
