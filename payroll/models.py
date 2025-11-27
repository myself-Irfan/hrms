from django.db import models
from employees.models import Employee
from tenants.models import Company

class SalaryStructure(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='salary_structure')
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    hra = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='salary_structures')

    def __str__(self):
        return f"Structure for {self.employee}"

class PayrollRecord(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='payroll_records')
    month = models.PositiveIntegerField()
    year = models.PositiveIntegerField()
    total_earnings = models.DecimalField(max_digits=10, decimal_places=2)
    total_deductions = models.DecimalField(max_digits=10, decimal_places=2)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='payroll_records')
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee} - {self.month}/{self.year}"
