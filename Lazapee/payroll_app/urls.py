"""
URL configuration for Lazapee project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.log_in, name = 'log_in'),
    path('landing', views.landing, name = 'landing'),
    path('log_out', views.log_out, name = 'log_out'),
    path('add_employee' , views.add_employee, name = 'add_employee'),
    path('remove_employee/<int:pk>/', views.remove_employee, name  = 'remove_employee'),
    path("add_overtime/<int:pk>/", views.add_overtime, name = 'add_overtime'),
    path('details/<int:pk>/', views.details, name = 'details'),
    path('edit_employee/<int:pk>', views.edit_employee, name = 'edit_employee'),
    path('payslips', views.payslips, name = 'payslips'),
    path('createSlip', views.createSlip, name = 'createSlip'),
    path('delete_slip/<int:pk>/', views.delete_slip, name = 'delete_slip'),
    path('register', views.register, name = 'register'),
    path('payDetails/<int:pk>/', views.payDetails, name = 'payDetails')
]
