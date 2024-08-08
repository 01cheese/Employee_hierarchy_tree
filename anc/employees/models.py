from django.db import models

# Определение модели Employee
class Employee(models.Model):
    # Полное имя сотрудника
    full_name = models.CharField(max_length=255)
    # Должность сотрудника
    position = models.CharField(max_length=255)
    # Дата найма сотрудника
    date_of_hire = models.DateField()
    # Электронная почта сотрудника
    email = models.EmailField()
    # Менеджер сотрудника, внешний ключ на ту же модель, позволяет создавать иерархию
    manager = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='subordinates')

    # Метод для отображения имени сотрудника
    def __str__(self):
        return self.full_name
