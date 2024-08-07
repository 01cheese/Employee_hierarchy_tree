from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from employees.views import home  # Імпортуйте представлення home
from employees import views as employee_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('employees/', include('employees.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', employee_views.register, name='register'),
    path('', employee_views.home, name='home'),  # Додайте це для головної сторінки
]
