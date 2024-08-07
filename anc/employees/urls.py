from django.urls import path
from .views import employee_tree, employee_list  # Імпортуйте ваші представлення тут

urlpatterns = [
    path('tree/', employee_tree, name='employee_tree'),
    path('list/', employee_list, name='employee_list'),
]
