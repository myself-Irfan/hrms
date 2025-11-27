from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/tenants/', include('tenants.urls')),
    path('api/employees/', include('employees.urls')),
    path('api/attendance/', include('attendance.urls')),
    path('api/leave/', include('leave.urls')),
    path('api/payroll/', include('payroll.urls')),
    path('api/notices/', include('notices.urls')),
    path('api/expenses/', include('expenses.urls')),
    # path('api/reports/', include('reports.urls')),
    # path('api/mobile/', include('mobile_api.urls')),
]
