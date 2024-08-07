from django.urls import path
from .views import employee_tree, employee_list, employee_subordinates
from django.urls import path
from . import views

urlpatterns = [
    path('', views.employee_list, name='employee_list'),
    path('tree/', employee_tree, name='employee_tree'),
    path('list/', employee_list, name='employee_list'),
    path('subordinates/<int:employee_id>/', employee_subordinates, name='employee_subordinates'),
    path('create/', views.employee_create, name='employee_create'),
    path('update/<int:pk>/', views.employee_update, name='employee_update'),
    path('delete/<int:pk>/', views.employee_delete, name='employee_delete'),
    path('update_manager/', views.update_manager, name='employee_update_manager'),
    path('search_managers/', views.search_managers, name='search_managers'),
]
