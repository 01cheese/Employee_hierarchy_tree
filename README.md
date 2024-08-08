
# Employee Management System

## Описание проекта

Employee Management System - это веб-приложение на Django, предназначенное для управления сотрудниками компании. Оно позволяет выполнять следующие функции:
- Регистрация новых пользователей
- Вход и выход пользователей
- Просмотр списка сотрудников
- Просмотр иерархии сотрудников
- Создание, обновление и удаление сотрудников

## Содержание

- [Технологии](#технологии)
- [Установка и настройка](#установка-и-настройка)
- [Описание моделей](#описание-моделей)
- [Формы](#формы)
- [Представления](#представления)
- [Маршруты](#маршруты)
- [Шаблоны](#шаблоны)
- [Заполнение базы данных](#заполнение-базы-данных)
- [Статические файлы](#статические-файлы)
- [Безопасность](#безопасность)
- [Скриншоты](#скриншоты)

## Технологии

Проект использует следующие технологии:

- Python 3.7+
- Django 3.2.25
- SQLite (встроенная база данных Django)
- Bootstrap 4.5.2 (для стилизации)
- jQuery 3.6.0 (для AJAX запросов)
- Select2 (для улучшения выбора менеджеров)
- Faker 18.13.0 (заполнение базы данных)

## Установка и настройка

Для начала работы с проектом, следуйте этим шагам:

1. **Клонирование репозитория**:
    ```bash
    git clone https://github.com/yourusername/employee-management-system.git
    cd employee-management-system
    ```

2. **Создание виртуального окружения**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # для Windows: venv\Scripts\activate
    ```

3. **Установка зависимостей**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Применение миграций**:
    ```bash
    python manage.py migrate
    ```

5. **Заполнение базы данных начальными данными**:
    ```bash
    python seed.py
    ```

6. **Запуск сервера разработки**:
    ```bash
    python manage.py runserver
    ```

Откройте браузер и перейдите по адресу `http://127.0.0.1:8000/` для просмотра приложения.

## Описание моделей

### Employee

Модель `Employee` представляет сотрудника компании. Она включает следующие поля:
- `full_name` (CharField): Полное имя сотрудника.
- `position` (CharField): Должность сотрудника.
- `date_of_hire` (DateField): Дата найма сотрудника.
- `email` (EmailField): Электронная почта сотрудника.
- `manager` (ForeignKey): Менеджер сотрудника, связанный с той же моделью, что позволяет строить иерархию.

```
class Employee(models.Model):
    full_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    date_of_hire = models.DateField()
    email = models.EmailField()
    manager = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='subordinates')

    def __str__(self):
        return self.full_name
```

## Формы

Для взаимодействия с моделью `Employee` используется форма `EmployeeForm`, которая наследуется от `forms.ModelForm`. Эта форма позволяет легко создавать и обновлять объекты модели `Employee`.

```
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['full_name', 'position', 'date_of_hire', 'email', 'manager']
```

## Представления

В приложении определено несколько представлений для различных функций. 

### Регистрация

Представление `register` обрабатывает регистрацию новых пользователей.

```
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

### Домашняя страница

Представление `home` отображает главную страницу приложения.

```
def home(request):
    return render(request, 'home.html')
```

### Список сотрудников

Представление `employee_list` отображает список всех сотрудников с возможностью поиска и сортировки.

```
@login_required
def employee_list(request):
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', 'full_name')
    page_number = request.GET.get('page', 1)
    items_per_page = request.GET.get('items_per_page', 50)

    if query:
        employees = Employee.objects.filter(
            Q(full_name__icontains=query) |
            Q(position__icontains=query) |
            Q(email__icontains=query)
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

### Иерархия сотрудников

Представление `employee_tree` отображает иерархию сотрудников в виде дерева.

```
@login_required
def employee_tree(request):
    top_level_employees = Employee.objects.filter(manager__isnull=True)
    context = {
        'top_level_employees': top_level_employees
    }
    return render(request, 'tree.html', context)
```

### Создание и обновление сотрудников

Представления `employee_create` и `employee_update` обрабатывают создание и обновление информации о сотрудниках.

```
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

### Удаление сотрудников

Представление `employee_delete` обрабатывает удаление сотрудников.

```
@login_required
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        return redirect('employee_list')
    return render(request, 'employee_confirm_delete.html', {'employee': employee})
```

## Маршруты

Основной файл маршрутизации `urls.py` и файл маршрутизации для приложения `employees`.

### Основной файл маршрутизации

```
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

### Маршруты для приложения `employees`

```
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

### JavaScript в `employee_tree.html`

Этот скрипт отвечает за динамическую загрузку и отображение подчиненных сотрудников в иерархическом виде.

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
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script>
        // Ждем полной загрузки документа
        $(document).ready(function() {
            // Добавляем обработчик события click для кнопок, которые раскрывают подчиненных
            $('.toggle-subordinates').click(function() {
                // Получаем текущую кнопку и идентификатор сотрудника
                var button = $(this);
                var employeeId = button.data('id');
                // Находим элемент списка, где будут отображены подчиненные
                var subordinatesList = $('#subordinates-' + employeeId);

                // Если подчиненные еще не загружены, загружаем их через AJAX
                if (subordinatesList.children().length === 0) {
                    $.ajax({
                        // URL для получения подчиненных
                        url: '{% url "employee_subordinates" 0 %}'.replace('0', employeeId),
                        method: 'GET',
                        success: function(data) {
                            // При успешном запросе добавляем подчиненных в список
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
                            // В случае ошибки выводим сообщение
                            alert('Error loading subordinates');
                        }
                    });
                } else {
                    // Если подчиненные уже загружены, просто скрываем или показываем их
                    subordinatesList.toggle();
                }
            });
        });
    </script>
</body>
</html>
```

#### Пояснение кода:

1. **Загрузка jQuery**:
    - `<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>` загружает библиотеку jQuery, которая упрощает работу с DOM и AJAX.

2. **Готовность документа**:
    - `$(document).ready(function() { ... });` - эта функция выполняется, когда весь документ загружен и готов к работе.

3. **Обработчик события click**:
    - `.click(function() { ... });` - назначает обработчик события click для элементов с классом `.toggle-subordinates`.

4. **Получение идентификатора сотрудника**:
    - `var employeeId = button.data('id');` - получает значение data-атрибута `id` кнопки, что позволяет определить, для какого сотрудника нужно загрузить подчиненных.

5. **AJAX запрос для загрузки подчиненных**:
    - `$.ajax({ ... });` - отправляет AJAX запрос на сервер для получения подчиненных сотрудников.

6. **Обработка успешного запроса**:
    - `success: function(data) { ... }` - эта функция выполняется при успешном запросе и добавляет полученных подчиненных в DOM.

7. **Обработка ошибки запроса**:
    - `error: function() { ... }` - эта функция выполняется при ошибке запроса и выводит сообщение об ошибке.

### JavaScript в `employee_form.html`

Этот скрипт отвечает за улучшение выбора менеджера с помощью Select2, что позволяет искать и выбирать менеджеров асинхронно.

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

#### Пояснение кода:

1. **Загрузка jQuery**:
    - `<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>` загружает библиотеку jQuery.

2. **Готовность документа**:
    - `$(document).ready(function() { ... });` - эта функция выполняется, когда весь документ загружен и готов к работе.

3. **Инициализация Select2**:
    - `$('.select2-ajax').select2({ ... });` - инициализирует Select2 на элементе с классом `select2-ajax`.

4. **Параметры Select2**:
    - `width: '100%'` - задает ширину элемента Select2.
    - `placeholder: "Select a manager"` - задает текст-заполнитель.
    - `allowClear: true` - позволяет очищать выбранное значение.

5. **AJAX запросы в Select2**:
    - `ajax: { ... }` - задает параметры для AJAX запросов.
    - `url: "{% url 'search_managers' %}"` - URL для поиска менеджеров.
    - `dataType: 'json'` - формат данных, возвращаемых с сервера.
    - `delay: 250` - задержка перед отправкой запроса (для предотвращения слишком частых запросов).
    - `data: function (params) { ... }` - функция для передачи параметров запроса.
    - `processResults: function (data) { ... }` - функция для обработки результатов запроса.
    - `cache: true` - кэширование запросов.

Этот JavaScript код улучшает взаимодействие пользователя с формой выбора менеджера, делая процесс поиска и выбора более удобным и быстрым.

## Шаблоны

### base.html

Основной шаблон, содержащий общую структуру для всех страниц.

```
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <

meta name="viewport" content="width=device-width, initial-scale=1.0">
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

### register.html

Шаблон для страницы регистрации.

```
{% extends 'base.html' %}

{% block title %}Register{% endblock %}

{% block content %}
<div class="card">
    <div class="card-header">
        <h1 class="h3">Register</h1>
    </div>
    <div class="card-body">
        <form method="post">
            {% csrf_token %}
            {{ form.as_p }}
            <button type="submit" class="btn btn-primary"><i class="fas fa-user-plus"></i> Register</button>
        </form>
    </div>
</div>
{% endblock %}
```

### employee_confirm_delete.html

Шаблон для подтверждения удаления сотрудника.

```
{% extends 'base.html' %}

{% block title %}Delete Employee{% endblock %}

{% block content %}
<div class="card">
    <div class="card-header">
        <h1 class="h3">Delete Employee</h1>
    </div>
    <div class="card-body">
        <p>Are you sure you want to delete {{ employee.full_name }}?</p>
        <form method="post">
            {% csrf_token %}
            <button type="submit" class="btn btn-danger"><i class="fas fa-trash-alt"></i> Delete</button>
            <a href="{% url 'employee_list' %}" class="btn btn-secondary"><i class="fas fa-arrow-left"></i> Cancel</a>
        </form>
    </div>
</div>
{% endblock %}
```

### home.html

Шаблон для домашней страницы.

```
{% extends 'base.html' %}

{% block title %}Home{% endblock %}

{% block content %}
<div class="jumbotron text-center bg-light">
    <h1 class="display-4">Welcome to the Employee Management System</h1>
    <p class="lead">Manage your company's employees efficiently and effectively.</p>
    <hr class="my-4">
    {% if user.is_authenticated %}
        <a class="btn btn-primary btn-lg" href="{% url 'employee_list' %}" role="button">View Employee List</a>
    {% else %}
        <a class="btn btn-primary btn-lg" href="{% url 'login' %}" role="button">Login</a>
        <a class="btn btn-secondary btn-lg" href="{% url 'register' %}" role="button">Register</a>
    {% endif %}
</div>
{% endblock %}
```

### login.html

Шаблон для страницы входа.

```
{% extends 'base.html' %}

{% block title %}Login{% endblock %}

{% block content %}
<div class="card">
    <div class="card-header">
        <h1 class="h3">Login</h1>
    </div>
    <div class="card-body">
        <form method="post">
            {% csrf_token %}
            <div class="form-group">
                <label for="id_username">Username:</label>
                <input type="text" name="username" class="form-control" id="id_username" required>
            </div>
            <div class="form-group">
                <label for="id_password">Password:</label>
                <input type="password" name="password" class="form-control" id="id_password" required>
            </div>
            <button type="submit" class="btn btn-primary"><i class="fas fa-sign-in-alt"></i> Login</button>
        </form>
        <p class="mt-3"><a href="{% url 'register' %}"><i class="fas fa-user-plus"></i> Register</a></p>
    </div>
</div>
{% endblock %}
```

### employee_list.html

Шаблон для отображения списка сотрудников.

```
{% extends 'base.html' %}

{% block title %}Employee List{% endblock %}

{% block content %}
<div class="d-flex justify-content-between align-items-center mb-3">
    <h1 class="h3">Employee List</h1>
    <a href="{% url 'employee_create' %}" class="btn btn-primary"><i class="fas fa-plus"></i> Add Employee</a>
</div>
<div class="table-responsive">
    <table class="table table-striped table-hover">
        <thead class="thead-dark">
            <tr>
                <th>Name</th>
                <th>Position</th>
                <th>Date of Hire</th>
                <th>Email</th>
                <th>Manager</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for employee in employees %}
                <tr>
                    <td>{{ employee.full_name }}</td>
                    <td>{{ employee.position }}</td>
                    <td>{{ employee.date_of_hire }}</td>
                    <td>{{ employee.email }}</td>
                    <td>{{ employee.manager.full_name|default_if_none:"None" }}</td>
                    <td>
                        <a href="{% url 'employee_update' employee.pk %}" class="btn btn-secondary btn-sm"><i class="fas fa-edit"></i> Edit</a>
                        <a href="{% url 'employee_delete' employee.pk %}" class="btn btn-danger btn-sm"><i class="fas fa-trash-alt"></i> Delete</a>
                    </td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}
```

### employee_tree.html

Шаблон для отображения иерархии сотрудников.

```
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
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script>
        $(document).ready(function() {
            $('.toggle-subordinates').click(function() {
                var button = $(this);
                var employeeId = button.data('id');
                var subordinatesList = $('#subordinates-' + employeeId);

                if (subordinatesList.children().length === 0) {
                    $.ajax({
                        url: '{% url "employee_subordinates" 0 %}'.replace('0',

 employeeId),
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

### employee_form.html

Шаблон для формы создания и редактирования сотрудника.

```
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

### subordinates.html

Включаемый шаблон для отображения подчиненных сотрудников.

```
<ul class="list-group ml-3">
    {% for subordinate in manager.subordinates.all %}
        <li class="list-group-item">
            <strong>{{ subordinate.full_name }}</strong> - {{ subordinate.position }}
            {% include 'subordinates.html' with manager=subordinate %}
        </li>
    {% endfor %}
</ul>
```

## Заполнение базы данных

Скрипт `seed.py` используется для заполнения базы данных начальными данными с помощью библиотеки `faker`.

```
import random
from faker import Faker

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'anc.settings')
django.setup()

from employees.models import Employee

faker = Faker()

def run():
    top_managers = [Employee.objects.create(
        full_name=faker.name(),
        position='Top Manager',
        hire_date=faker.date_this_century(),
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
                hire_date=faker.date_this_century(),
                email=faker.email(),
                manager=manager
            )
            add_subordinates(employee, level + 1)

    for manager in top_managers:
        add_subordinates(manager, 1)

if __name__ == "__main__":
    run()
```

## Статические файлы

### custom.css

Кастомные стили для проекта.

```
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

## Безопасность

- **CSRF защита**: Включена по умолчанию в Django и используется в формах.
- **Валидация форм**: Используется встроенная валидация Django.
- **Аутентификация и авторизация**: Используется встроенная система аутентификации Django.

## Скриншоты

![image](https://github.com/user-attachments/assets/62a4504f-4048-4615-9fd1-6373dab535dc)

![image](https://github.com/user-attachments/assets/75562212-ab8d-480d-b7de-13a9ac08e594)

![image](https://github.com/user-attachments/assets/2ed636b8-4ea6-4db8-a6fc-8b330ac91d93)

### Главная страница

![image](https://github.com/user-attachments/assets/e0206ff5-24b9-4a34-8bf5-230b5eec4cb1)

### Список сотрудников

![image](https://github.com/user-attachments/assets/b993e561-afe8-485d-89f4-b0bc56cee7d8)


### Форма создания или изминения сотрудника

![image](https://github.com/user-attachments/assets/d6f9a4d7-bb85-499d-91e7-3ff6a357fa7f)


### Иерархия сотрудников

![image](https://github.com/user-attachments/assets/a389603a-8589-46a5-a45d-3fd0caad7a46)


### Поиск

![image](https://github.com/user-attachments/assets/c8ff00a7-60bb-4783-9e1c-259955a73fae)

### Удаление

![image](https://github.com/user-attachments/assets/50a58b6b-9959-4a84-b944-69b77d057855)

### Возможность передвигать учасников

![image](https://github.com/user-attachments/assets/922eeda3-a0ef-4f06-8c92-0dd11d5919bf)
