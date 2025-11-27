from rest_framework import viewsets
from .models import Expense
from .serializers import ExpenseSerializer
from employees.views import BaseCompanyViewSet

class ExpenseViewSet(BaseCompanyViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'superadmin':
            return Expense.objects.all()
        if user.role == 'employee':
            return Expense.objects.filter(employee__user=user)
        if user.company:
            return Expense.objects.filter(company=user.company)
        return Expense.objects.none()
