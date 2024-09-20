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

def prices_create(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    user = request.user
    prices = Price.objects.all()

    if request.method == 'POST':
        form = PriceForm(request.POST, project=project, user=user)
        print(form.errors)
        if form.is_valid():
            price = form.save(commit=False)
            price.project = project
            price.save()
            price.user.add(request.user)
            messages.info(request, f"Price created successfully.")
            return redirect((reverse('prices_create', args=[project_id])))
        else:
            messages.error(request,"Fail to create the Price.")
    else:
        form = PriceForm(project=project, user=user)
        

    return render(request, 'prices/prices_create.html', {'form': form, 'project': project, 'prices': prices, 'project_id': project_id})


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
        print(data)

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
    
def tasks_delete(request, pk, project_id):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        messages.success(request, f"Task created successfully.")
        return redirect((reverse('task_create', args=[project_id])))
    return render(request, 'prices/task_delete.html', {'task': task, 'pk': pk})

def tasks_detail(request, pk, project_id):
    task = get_object_or_404(Task, pk=pk)
    prices = Price.objects.all().order_by('code')
    components = TaskComponent.objects.filter(task_id=pk)
    currency_instance = Currency.objects.first()

    task_obj = Task.objects.filter(id=pk)
    for item in task_obj:
        task_currency = item.currency
    
       
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
            price_number = price_obj.price
            price_denomination = price_obj.denomination
            price_unit = price_obj.unit
            price_currency = price_obj.currency
            print("price before: ", price_number)
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

            print("price after: ", price_number)

        quantities.append(quantity)
        denominations.append(price_denomination)
        units.append(price_unit)
        prices_comp.append(price_number)
        grand_total += quantity * Decimal(price_number)

        task.price = round(grand_total, 2)
        task.save()
        
    
    
    grand_total = "{:,.2f}".format(grand_total)

    zipped_data = zip(components, denominations, units, prices_comp)


    
    return render(request, 'prices/tasks_detail.html', {'task': task, 'project_id': project_id, 'prices': prices, 'components': components, 'zipped_data': zipped_data, 'grand_total': grand_total})

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
    print("Component id: ", comp_id)
    comp = get_object_or_404(TaskComponent, pk=comp_id)
    if request.method == 'POST':
        comp.delete()
        messages.success(request, f"Task created successfully.")
        return redirect('tasks_detail', project_id=project_id, pk=pk)
    return render(request, 'prices/task_delete.html', {'comp': comp, 'pk': comp_id})