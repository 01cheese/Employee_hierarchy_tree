from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from employees.views import home
from employees import views as employee_views

# Маршруты основного приложения
urlpatterns = [
    path('admin/', admin.site.urls),  # Админка
    path('employees/', include('employees.urls')),  # Маршруты для приложения employees
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),  # Вход
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Выход
    path('register/', employee_views.register, name='register'),  # Регистрация
    path('', employee_views.home, name='home'),  # Главная страница
]
