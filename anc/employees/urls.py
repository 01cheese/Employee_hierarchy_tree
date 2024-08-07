from django.urls import path
from .views import employee_tree, employee_list, employee_subordinates

urlpatterns = [
    path('tree/', employee_tree, name='employee_tree'),
    path('list/', employee_list, name='employee_list'),
    path('subordinates/<int:employee_id>/', employee_subordinates, name='employee_subordinates'),
]
