from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import PriceForm, TaskForm, ComponentForm
from .models import Project, Price, Task, TaskComponent
from tasks.models import Currency
from django.http import JsonResponse
import json
from django.views.generic import ListView, CreateView
from django.contrib import messages
from decimal import Decimal
from workpackage.models import WorkPackage, WorkpackageTotals, Work

def prices_create(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    user = request.user
    # prices = Price.objects.all().order_by('code')
    # Sorting fields
    sort_field = request.GET.get('sort', 'code') # Default sorting by 'code'
    search_term = request.GET.get('search', '')  # Default to empty string if no search term
    # Validate the sort field to avoid SQL injection
    valid_sort_fields = ['id', 'code', 'denomination', 'price', 'currency', 'unit', 'tag', 'reference']
    if sort_field not in valid_sort_fields:
        sort_field = 'code'  # Fallback to default if invalid

    # Fetch prices related to the project and filter by the search term
    prices = Price.objects.filter(project=project)

    if search_term:
        prices = prices.filter(denomination__icontains=search_term)  # Case-insensitive search

    # Order the prices based on the sort field
    prices = prices.order_by(sort_field)
    
    if request.method == 'POST':
        form = PriceForm(request.POST, project=project, user=user)
        print(form.errors)
        if form.is_valid():
            price = form.save(commit=False)
            price.project = project
            price.save()
            price.user.add(request.user)
            messages.success(request, f"Component created successfully.")
            return redirect((reverse('prices_create', args=[project_id])))
        else:
            messages.error(request,"Fail to create the Component.")
    else:
        form = PriceForm(project=project, user=user)
        

    return render(request, 'prices/prices_create.html', {'form': form, 'project': project, 'prices': prices, 'project_id': project_id})

# Adding 1 to the last code
def get_last_code(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    last_price = Price.objects.filter(project=project).order_by('-id').first()
    # -id, meaning to look in descending order
    if last_price:
        last_code = last_price.code
    else:
        last_code = "000000_00M"  # Default starting code, adjust as needed

    return JsonResponse({'last_code': last_code})


def prices_delete(request, pk, project_id):
    price = get_object_or_404(Price, pk=pk)
    if request.method == 'POST':
        price.delete()
        return redirect('prices_create', project_id)
    return render(request, 'prices/prices_delete.html', {'price': price, 'pk': pk})


def prices_update_database(request):
    if request.method == 'POST':
        # Get the data from the request
        data = json.loads(request.body.decode('utf-8'))        
        # Extract the data from the JSON object
        price_id = data.get('price_id')
        field_name = data.get('field_name')
        value = data.get('value')

        # Get the Price object from the database
        price_obj = Price.objects.get(id=price_id)

        # Update the Price object with the new value
        setattr(price_obj, field_name, value)
        price_obj.save()

        # Return a JSON response to indicate success
        return JsonResponse({'message': 'Price updated successfully'})

    else:
        # Return a JSON response to indicate an error
        return JsonResponse({'message': 'Invalid request'}, status=400)

def task_component_quantity_update(request):
    if request.method == 'POST':
        # Get the data from the request
        data = json.loads(request.body.decode('utf-8'))
        
        # Extract the data from the JSON object
        taskcomponent_id = data.get('id')
        field_name = data['name'] 
        value = data.get('value')

        # Get the Price object from the database
        taskcomponent_obj = TaskComponent.objects.get(id=taskcomponent_id)

        # Update the Price object with the new value
        setattr(taskcomponent_obj, field_name, value)
        taskcomponent_obj.save()

        # Return a JSON response to indicate success
        return JsonResponse({'message': 'Component Quantity updated successfully'})

    else:
        # Return a JSON response to indicate an error
        return JsonResponse({'message': 'Invalid request'}, status=400)
    
def trial(request):
    return render(request, 'prices/trial.html')


def task_create(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    tasks = Task.objects.all()
    
    if request.method == 'POST':
        form = TaskForm(request.POST)
        print(form.errors)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.currency = project.currency
            task.save()
            messages.success(request, f"Task created successfully.")
            return redirect((reverse('task_create', args=[project_id])))
        else:
            messages.error(request,"Fail to create the Task.")
    else:
        initial_data = {'currency': project.currency}
        form = TaskForm(initial=initial_data)

    
    return render(request, 'prices/tasks_list.html', {'form': form, 'tasks': tasks, 'project': project,'project_id': project_id})


def recalculate_workpackage_totals(work_package):
    # Get all Work instances related to the work package
    works = Work.objects.filter(work_package=work_package)
    
    # Calculate the grand total
    quantities_list = [work.quantity for work in works]
    prices_list = [work.task.price for work in works.select_related('task')]
    
    grand_total = sum(q * p for q, p in zip(quantities_list, prices_list))
        
    # Update or create the WorkpackageTotals entry
    wp_budget, created = WorkpackageTotals.objects.update_or_create(
        workpackage=work_package,
        defaults={'total': grand_total}
    )

def tasks_delete(request, pk, project_id):
    task = get_object_or_404(Task, pk=pk)

    # Get all Work instances related to the task
    works = Work.objects.filter(task=task)

    # Get all related work packages
    work_packages = WorkPackage.objects.filter(work__in=works).distinct()

    if request.method == 'POST':
        task.delete()
        try:
            work_packages = WorkPackage.objects.all()
            for wp in work_packages:
                recalculate_workpackage_totals(wp)

            messages.success(request, "Task deleted successfully.")
        except Exception as e:
            messages.error(request, "An error occurred while deleting the task.")
        
        return redirect(reverse('task_create', args=[project_id]))

    return render(request, 'prices/tasks_delete.html', {'task': task, 'pk': pk})

def tasks_detail(request, pk, project_id):
    task = get_object_or_404(Task, pk=pk)
    prices = Price.objects.all().order_by('code')
    components = TaskComponent.objects.filter(task_id=pk)
    currency_instance = Currency.objects.first()
    
    task_obj = Task.objects.filter(id=pk)
    
    for item in task_obj:
        task_currency = item.currency

    id = []   
    denominations = []
    units = []
    prices_comp = []
    quantities = []
    grand_total = 0 


    for component in components:
        component_code = component.code_id
        quantity = Decimal(component.quantity)

        all_price_objs = Price.objects.filter(pk=component_code)
        for price_obj in all_price_objs:
            price_id = price_obj.id
            price_number = price_obj.price
            price_denomination = price_obj.denomination
            price_unit = price_obj.unit
            price_currency = price_obj.currency
            # Checking the currencys
            if task_currency != price_currency:
                if task_currency == "USD" and price_currency == "SAR":
                    rate = Decimal(currency_instance.usd_sar)
                    price_number = round(price_number * ( 1 / rate), 2)
                elif task_currency == "USD" and price_currency == "EUR":
                    rate = (currency_instance.eur_usd)
                    price_number = round(price_number * rate, 2)
                elif task_currency == "EUR" and price_currency == "SAR":
                    rate = Decimal(currency_instance.eur_sar)
                    price_number = round(price_number * ( 1 / rate), 2)
                elif task_currency == "EUR" and price_currency == "USD":
                    rate = Decimal(currency_instance.eur_usd)
                    price_number = round(price_number * ( 1 / rate), 2)
                elif task_currency == "SAR" and price_currency == "USD":
                    rate = Decimal(currency_instance.usd_sar)
                    price_number = round(price_number * rate, 2)
                elif task_currency == "SAR" and price_currency == "EUR":
                    rate = Decimal(currency_instance.eur_sar)
                    price_number = round(price_number * rate, 2)
        id.append(price_id)
        quantities.append(quantity)
        denominations.append(price_denomination)
        units.append(price_unit)
        prices_comp.append(price_number)
        grand_total += quantity * Decimal(price_number)

        task.price = round(grand_total, 2)
        task.save()
    
    grand_total = "{:,.2f}".format(grand_total)

    zipped_data = zip(id, components, denominations, units, prices_comp)

    return render(request, 'prices/tasks_detail.html', {
        'task': task, 
        'project_id': project_id, 
        'prices': prices, 
        'components': components, 
        'zipped_data': zipped_data, 
        'grand_total': grand_total
        })

def tasks_add_component(request, project_id, pk):
    task = get_object_or_404(Task, pk=pk)    
    if request.method == 'POST':
        form = ComponentForm(request.POST)
        print(form.errors)
        if form.is_valid():
            cleaned_data = form.cleaned_data            
            task_component = TaskComponent(task=task, code=cleaned_data['code'], quantity=cleaned_data['quantity'])
            task_component.save()
            messages.success(request, f"Component added successfully.")
            return redirect('tasks_detail', project_id=project_id, pk=pk)
        else:
            messages.error(request,"Fail to add the Component.")
    else:
        form = ComponentForm()
    return render(request, 'prices/tasks_detail.html', {'form': form, 'project_id': project_id, 'task': task})


def tasks_comp_delete(request, pk, comp_id, project_id):
    comp = get_object_or_404(TaskComponent, pk=comp_id)
    if request.method == 'POST':
        comp.delete()
        messages.success(request, f"Component deleted successfully.")
        return redirect('tasks_detail', project_id=project_id, pk=pk)
    return render(request, 'prices/task_delete.html', {'comp': comp, 'pk': comp_id})

def task_name_update(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        task_id = data['id']
        task_field = data['name']
        task_value = data['value']
        
        task_obj = Task.objects.get(id=task_id)
        if task_field == 'name':
            task_obj.name = task_value
        elif task_field == 'code':
            task_obj.code = task_value
        elif task_field == 'price':
            task_obj.price = task_value
        elif task_field == 'unit':
            task_obj.unit = task_value
        task_obj.save()

        messages.success(request, 'Task updated successfully!')
        return JsonResponse({'message': 'Task updated successfully!'})
    else:
        messages.error(request, 'Task was not updated')
    return JsonResponse({'message': 'Invalid request in updateTaskName'})