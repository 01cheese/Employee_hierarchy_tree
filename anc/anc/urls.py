from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from employees.views import home  # Імпортуйте представлення home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('employees/', include('employees.urls')),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', home, name='home'),  # Додайте маршрут для кореневого URL
]
