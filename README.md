```
Here’s the English translation and the full structure for the Employee Management System project file:

```markdown
# Employee Management System

## Project Description

The Employee Management System is a Django-based web application designed to manage company employees. It provides the following functionality:
- User registration
- User login and logout
- View the list of employees
- View the hierarchy of employees
- Create, update, and delete employees

## Table of Contents

- [Technologies](#technologies)
- [Installation and Setup](#installation-and-setup)
- [Model Descriptions](#model-descriptions)
- [Forms](#forms)
- [Views](#views)
- [URLs](#urls)
- [Templates](#templates)
- [Database Seeding](#database-seeding)
- [Static Files](#static-files)
- [Security](#security)
- [Screenshots](#screenshots)

## Technologies

The project uses the following technologies:

- Python 3.7+
- Django 3.2.25
- SQLite (Django's built-in database)
- Bootstrap 4.5.2 (for styling)
- jQuery 3.6.0 (for AJAX requests)
- Select2 (for enhanced manager selection)
- Faker 18.13.0 (for database seeding)

## Installation and Setup

To get started with the project, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/employee-management-system.git
    cd employee-management-system
    ```

2. **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # for Windows: venv\Scripts\activate
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Apply migrations**:
    ```bash
    python manage.py migrate
    ```

5. **Seed the database with initial data**:
    ```bash
    python seed.py
    ```

6. **Start the development server**:
    ```bash
    python manage.py runserver
    ```

Open your browser and navigate to `http://127.0.0.1:8000/` to view the application.

## Model Descriptions

### Employee

The `Employee` model represents a company employee. It includes the following fields:
- `full_name` (CharField): The employee’s full name.
- `position` (CharField): The employee’s position.
- `date_of_hire` (DateField): The date the employee was hired.
- `email` (EmailField): The employee’s email address.
- `manager` (ForeignKey): The employee’s manager, related to the same model, allowing the creation of a hierarchy.

```python
class Employee(models.Model):
    full_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    date_of_hire = models.DateField()
    email = models.EmailField()
    manager = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='subordinates')

    def __str__(self):
        return self.full_name
```

## Forms

The `EmployeeForm` is used to interact with the `Employee` model. It inherits from `forms.ModelForm` and simplifies creating and updating employee objects.

```python
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['full_name', 'position', 'date_of_hire', 'email', 'manager']
```

## Views

Several views are defined in the application for different functions.

### Registration

The `register` view handles user registration.

```python
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('employee_list')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
```

### Home Page

The `home` view renders the application’s home page.

```python
def home(request):
    return render(request, 'home.html')
```

### Employee List

The `employee_list` view displays a list of all employees with search and sorting options.

```python
@login_required
def employee_list(request):
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', 'full_name')
    page_number = request.GET.get('page', 1)
    items_per_page = request.GET.get('items_per_page', 50)

    if query:
        employees = Employee.objects.filter(
            Q(full_name__icontains=query) |
            Q(position__icontains(query) |
            Q(email__icontains(query)
        ).order_by(sort_by)
    else:
        employees = Employee.objects.all().order_by(sort_by)

    paginator = Paginator(employees, items_per_page)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
        'sort_by': sort_by,
        'items_per_page': items_per_page
    }
    return render(request, 'list.html', context)
```

### Employee Hierarchy

The `employee_tree` view displays an employee hierarchy in a tree structure.

```python
@login_required
def employee_tree(request):
    top_level_employees = Employee.objects.filter(manager__isnull=True)
    context = {
        'top_level_employees': top_level_employees
    }
    return render(request, 'tree.html', context)
```

### Create and Update Employees

The `employee_create` and `employee_update` views handle the creation and updating of employee information.

```python
@login_required
def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'employee_form.html', {'form': form})

@login_required
def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employee_form.html', {'form': form})
```

### Delete Employees

The `employee_delete` view handles the deletion of employees.

```python
@login_required
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        return redirect('employee_list')
    return render(request, 'employee_confirm_delete.html', {'employee': employee})
```

## URLs

The main `urls.py` file and the app-specific `urls.py` for the `employees` app.

### Main URL File

```python
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from employees.views import home
from employees import views as employee_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('employees/', include('employees.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', employee_views.register, name='register'),
    path('', employee_views.home, name='home'),
]
```

### Employee App URL File

```python
from django.urls import path
from .views import employee_tree, employee_list, employee_subordinates
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
```

### JavaScript for `employee_tree.html`

This script dynamically loads and displays subordinates in a hierarchical view.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Employee Hierarchy</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            font-family: Arial, sans-serif;
        }
        .container {
            margin-top: 50px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Employee Hierarchy</h1>
        <ul id="employee-tree">
            {% include 'subordinates.html' with employees=employees %}
        </ul>
        <a href="{% url 'employee_list' %}" class="btn btn-secondary">Back to List</a>
    </div>
    <script src

="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script>
        $(document).ready(function() {
            $('.toggle-subordinates').click(function() {
                var button = $(this);
                var employeeId = button.data('id');
                var subordinatesList = $('#subordinates-' + employeeId);

                if (subordinatesList.children().length === 0) {
                    $.ajax({
                        url: '{% url "employee_subordinates" 0 %}'.replace('0', employeeId),
                        method: 'GET',
                        success: function(data) {
                            data.forEach(function(subordinate) {
                                var listItem = $('<li>').text(subordinate.full_name + ' - ' + subordinate.position);
                                var subButton = $('<button>').text('Toggle Subordinates').addClass('btn btn-link toggle-subordinates').attr('data-id', subordinate.id);
                                listItem.append(subButton);
                                var subList = $('<ul>').attr('id', 'subordinates-' + subordinate.id);
                                listItem.append(subList);
                                subordinatesList.append(listItem);
                            });
                        },
                        error: function() {
                            alert('Error loading subordinates');
                        }
                    });
                } else {
                    subordinatesList.toggle();
                }
            });
        });
    </script>
</body>
</html>
```

### JavaScript in `employee_form.html`

This script enhances manager selection using Select2, allowing users to search for and select managers asynchronously.

```html
{% extends 'base.html' %}

{% block title %}{{ form_title }}{% endblock %}

{% block content %}
<div class="card">
    <div class="card-header">
        <h1 class="h3">{{ form_title }}</h1>
    </div>
    <div class="card-body">
        <form method="post">
            {% csrf_token %}
            <div class="form-group">
                <label for="id_full_name">Full name:</label>
                <input type="text" name="full_name" value="{{ form.full_name.value }}" class="form-control" id="id_full_name">
            </div>
            <div class="form-group">
                <label for="id_position">Position:</label>
                <input type="text" name="position" value="{{ form.position.value }}" class="form-control" id="id_position">
            </div>
            <div class="form-group">
                <label for="id_date_of_hire">Date of hire:</label>
                <input type="date" name="date_of_hire" value="{{ form.date_of_hire.value }}" class="form-control" id="id_date_of_hire">
            </div>
            <div class="form-group">
                <label for="id_email">Email:</label>
                <input type="email" name="email" value="{{ form.email.value }}" class="form-control" id="id_email">
            </div>
            <div class="form-group">
                <label for="id_manager">Manager:</label>
                <select name="manager" class="form-control select2-ajax" id="id_manager"></select>
            </div>
            <button type="submit" class="btn btn-primary"><i class="fas fa-save"></i> Save</button>
        </form>
        <a href="{% url 'employee_list' %}" class="btn btn-secondary mt-3"><i class="fas fa-arrow-left"></i> Back to List</a>
    </div>
</div>
<script>
    $(document).ready(function() {
        $('.select2-ajax').select2({
            width: '100%',
            placeholder: "Select a manager",
            allowClear: true,
            ajax: {
                url: "{% url 'search_managers' %}",
                dataType: 'json',
                delay: 250,
                data: function (params) {
                    return {
                        q: params.term
                    };
                },
                processResults: function (data) {
                    return {
                        results: data.results
                    };
                },
                cache: true
            }
        });
    });
</script>
{% endblock %}
```

## Templates

### base.html

The base template containing the general structure for all pages.

```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Employee Management{% endblock %}</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" rel="stylesheet">
    <link href="{% static 'css/custom.css' %}" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <a class="navbar-brand" href="{% url 'home' %}">Employee Management</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ml-auto">
                {% if user.is_authenticated %}
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'employee_list' %}"><i class="fas fa-users"></i> Employees</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'logout' %}"><i class="fas fa-sign-out-alt"></i> Logout</a>
                    </li>
                {% else %}
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'login' %}"><i class="fas fa-sign-in-alt"></i> Login</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'register' %}"><i class="fas fa-user-plus"></i> Register</a>
                    </li>
                {% endif %}
            </ul>
        </div>
    </nav>
    <div class="container mt-5">
        {% if messages %}
            <div class="alert alert-info" role="alert">
                {% for message in messages %}
                    {{ message }}
                {% endfor %}
            </div>
        {% endif %}
        {% block content %}{% endblock %}
    </div>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

### Other Templates

Additional templates for registration, login, employee listing, form handling, etc., follow the same structure as above with customized content.

## Database Seeding

The `seed.py` script is used to populate the database with initial data using the `faker` library.

```python
import random
from faker import Faker
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()

from employees.models import Employee

faker = Faker()

def run():
    top_managers = [Employee.objects.create(
        full_name=faker.name(),
        position='Top Manager',
        date_of_hire=faker.date_this_century(),
        email=faker.email(),
        manager=None
    ) for _ in range(10)]

    def add_subordinates(manager, level):
        if level > 7:
            return
        num_subordinates = random.randint(5, 10)
        for _ in range(num_subordinates):
            employee = Employee.objects.create(
                full_name=faker.name(),
                position=f'Level {level} Employee',
                date_of_hire=faker.date_this_century(),
                email=faker.email(),
                manager=manager
            )
            add_subordinates(employee, level + 1)

    for manager in top_managers:
        add_subordinates(manager, 1)

if __name__ == "__main__":
    run()
```

## Static Files

### custom.css

Custom styles for the project.

```css
body {
    font-family: 'Roboto', sans-serif;
}

.card {
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    border: none;
}

.table th, .table td {
    vertical-align: middle;
}

.navbar-brand {
    font-weight: bold;
    color: #ffffff !important;
}

.nav-link {
    font-weight: 500;
    color: #ffffff !important;
}

.btn-primary {
    background-color: #007bff;
    border-color: #007bff;
}

.btn-primary:hover {
    background-color: #0056b3;
    border-color: #0056b3;
}

.alert-info {
    background-color: #d1ecf1;
    border-color: #bee5eb;
    color: #0c5460;
}

.jumbotron {
    background: #f8f9fa;
    border-radius: 0.3rem;
    padding: 2rem 1rem;
    margin-bottom: 2rem;
}
```

## Security

- **CSRF protection**: Enabled by default in Django and used in forms.
- **Form validation**: Utilizes Django’s built-in validation.
- **Authentication and authorization**: Uses Django’s built-in authentication system.

## Screens

```

## 

![image](https://github.com/user-attachments/assets/62a4504f-4048-4615-9fd1-6373dab535dc)

![image](https://github.com/user-attachments/assets/75562212-ab8d-480d-b7de-13a9ac08e594)

![image](https://github.com/user-attachments/assets/2ed636b8-4ea6-4db8-a6fc-8b330ac91d93)

### Main page

![image](https://github.com/user-attachments/assets/e0206ff5-24b9-4a34-8bf5-230b5eec4cb1)

### Main list

![image](https://github.com/user-attachments/assets/b993e561-afe8-485d-89f4-b0bc56cee7d8)


### Form for createor edit employee

![image](https://github.com/user-attachments/assets/d6f9a4d7-bb85-499d-91e7-3ff6a357fa7f)


### Employee hierarchy

![image](https://github.com/user-attachments/assets/a389603a-8589-46a5-a45d-3fd0caad7a46)


### Search

![image](https://github.com/user-attachments/assets/c8ff00a7-60bb-4783-9e1c-259955a73fae)

### Delete

![image](https://github.com/user-attachments/assets/50a58b6b-9959-4a84-b944-69b77d057855)

### Ability to move participants

![image](https://github.com/user-attachments/assets/922eeda3-a0ef-4f06-8c92-0dd11d5919bf)
