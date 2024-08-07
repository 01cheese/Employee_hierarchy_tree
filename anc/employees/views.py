from django.shortcuts import render
from employees.models import Employee
from django.db.models import Q
from django.core.paginator import Paginator


def home(request):
    return render(request, 'home.html')


def employee_tree(request):
    top_level_employees = Employee.objects.filter(manager__isnull=True)
    context = {
        'top_level_employees': top_level_employees
    }
    return render(request, 'tree.html', context)


def employee_list(request):
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', 'full_name')
    page_number = request.GET.get('page', 1)
    items_per_page = request.GET.get('items_per_page', 50)  # Кількість записів на сторінку, за замовчуванням 50

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
