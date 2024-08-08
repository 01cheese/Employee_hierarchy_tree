from django import forms
from .models import Employee

# Форма для модели Employee
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee  # Указываем модель, на основе которой будет создана форма
        fields = ['full_name', 'position', 'date_of_hire', 'email', 'manager']  # Поля, которые будут включены в форму
