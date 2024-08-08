from django.urls import path
from .views import employee_tree, employee_list, employee_subordinates
from . import views

# Маршруты для приложения employees
urlpatterns = [
    path('', views.employee_list, name='employee_list'),  # Список сотрудников
    path('tree/', employee_tree, name='employee_tree'),  # Иерархия сотрудников
    path('list/', employee_list, name='employee_list'),  # Список сотрудников (дублируется)
    path('subordinates/<int:employee_id>/', employee_subordinates, name='employee_subordinates'),  # Подчиненные сотрудника
    path('create/', views.employee_create, name='employee_create'),  # Создание сотрудника
    path('update/<int:pk>/', views.employee_update, name='employee_update'),  # Обновление сотрудника
    path('delete/<int:pk>/', views.employee_delete, name='employee_delete'),  # Удаление сотрудника
    path('update_manager/', views.update_manager, name='employee_update_manager'),  # Обновление менеджера
    path('search_managers/', views.search_managers, name='search_managers'),  # Поиск менеджеров
]
