from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Employee
from django.shortcuts import render, get_object_or_404, redirect
from .models import Employee
from .forms import EmployeeForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect



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
    return render(request, 'registration/register.html', {'form': form})

def home(request):
    return render(request, 'home.html')


@login_required
def employee_tree(request):
    top_level_employees = Employee.objects.filter(manager__isnull=True)
    context = {
        'top_level_employees': top_level_employees
    }
    return render(request, 'tree.html', context)


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



def search_managers(request):
    if request.is_ajax():
        query = request.GET.get('q', '')
        managers = Employee.objects.filter(full_name__icontains=query)[:10]  # Обмежимо кількість результатів
        results = []
        for manager in managers:
            manager_json = {}
            manager_json['id'] = manager.id
            manager_json['text'] = manager.full_name
            results.append(manager_json)
        return JsonResponse({'results': results})
    return JsonResponse({'results': []})



def employee_subordinates(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    subordinates = list(employee.subordinates.values('id', 'full_name', 'position'))
    return JsonResponse(subordinates, safe=False)


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
            print("Form is valid and saved")
            return redirect('employee_list')
        else:
            print("Form is invalid")
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employee_form.html', {'form': form})

@login_required
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        return redirect('employee_list')
    return render(request, 'employee_confirm_delete.html', {'employee': employee})


@csrf_exempt
@login_required
def update_manager(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        new_manager_id = request.POST.get('new_manager_id')
        try:
            employee = Employee.objects.get(pk=employee_id)
            new_manager = Employee.objects.get(pk=new_manager_id)
            employee.manager = new_manager
            employee.save()
            return JsonResponse({'status': 'success'})
        except Employee.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Employee not found'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)