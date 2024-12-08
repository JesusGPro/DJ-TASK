from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.forms import ModelForm
from .models import WorkPackage, WorkLevel, Work, Measurement, WorkpackageTotals
from .forms import WorkLevelForm, WorkPackageForm, WorkForm, WPIdForm, MeasurementForm, CopyWorkForm, CopyWorkPackageForm
from tasks.models import ActiveProject, Project
from prices.models import Task, TaskComponent
from django.http import JsonResponse, HttpResponse
from django.forms.formsets import formset_factory
import json
from decimal import Decimal

############# BUDGET ##################################################################
def budget_assign(request):
    active_project = ActiveProject.objects.get(user=request.user)
    project_id = active_project.project_id
    project = Project.objects.get(id=project_id)
    project_description = project.description
    wps = WorkPackage.objects.all().order_by('name')
   
    if request.method == 'POST':
        form = WPIdForm(request.POST)
        print(form.errors)
        if form.is_valid():
            work_package_id = form.cleaned_data['work_package_id']
            return redirect('budget_create', work_package_id=work_package_id)
    else:
        form = WPIdForm()
    return render(request, 'workpackage/budget_assign.html', {
        'form': form,
        'project_id': project_id, 
        'project_description': project_description,
        'wps': wps
        })

def budget_create(request, work_package_id):
    active_project = ActiveProject.objects.get(user=request.user)
    project_id = active_project.project_id
    project = Project.objects.get(id=project_id)
    project_description = project.description

    work_package = WorkPackage.objects.get(id=work_package_id)
    tasks = Task.objects.all()
    form = WorkForm()

    # Sending elements to the list
    works = Work.objects.filter(work_package = work_package_id).select_related('task')
    task_ids = list(Work.objects.filter(work_package = work_package_id).values_list('task_id', flat=False))
    task_ids = [task_id[0] for task_id in task_ids]
    tasks_retrieved = sorted(Task.objects.filter(id__in=task_ids), key=lambda x: task_ids.index(x.id))
    zips = list(zip(works, tasks_retrieved))

    # calculating the grand total of the chapter:   
    quantities_list = []
    for q in works:
        quantities_list.append(q.quantity)
    
    prices_list = []
    for p in task_ids:
        price = Task.objects.get(id=p).price
        prices_list.append(price)
    
    grand_total = 0
    for i in range(0, len(quantities_list)):
        grand_total += quantities_list[i] * prices_list[i]

    # Storing in the data base, first check if it exist, if exists only update
    wp_budget =WorkpackageTotals(total=grand_total, workpackage_id=work_package_id)
    if WorkpackageTotals.objects.filter(workpackage_id=work_package_id).exists():
        existing_wp_budget = WorkpackageTotals.objects.get(workpackage_id=work_package_id)
        existing_wp_budget.total = grand_total
        existing_wp_budget.save()
    else:
        wp_budget.save()

    # Update or create the WorkpackageTotals
    wp_budget, created = WorkpackageTotals.objects.update_or_create(
        workpackage=work_package,
        defaults={'total': grand_total}
    )
    
    formatted_grand_total = "{:,.2f}".format(grand_total)


    if request.method == 'POST':
        form = WorkForm(request.POST)
        print(form.errors)
        if form.is_valid():
            task = form.cleaned_data['task']
            task_id = task.id
            quantity = form.cleaned_data['quantity']

            # Check if a work with the same task_id already exists
            if Work.objects.filter(task_id=task_id, work_package=work_package).exists():
                messages.error(request, 'A work with the same task ID already exists.')
                return redirect(reverse('budget_create', args=[work_package_id]))

            budget = Work(
                work_package=work_package,
                task_id=task_id,
                quantity=quantity,
            )
            budget.save()
            messages.success(request, 'Work created successfully!')

            # Recalculate the grand total after adding the new work
            works = Work.objects.filter(work_package=work_package_id).select_related('task')
            grand_total = sum(work.work_amount for work in works)

            # Update the WorkpackageTotals
            wp_budget.total = grand_total
            wp_budget.save()

            return redirect(reverse('budget_create', args=[work_package_id]))
        else:
            messages.error(request, 'Work could not be created.')
            form = WorkForm()

    return render(request, 'workpackage/budget_create.html', {
        'project_id': project_id,
        'project_description': project_description,
        'work_package_id': work_package_id,
        'work_package_name': work_package.name,
        'work_package_description': work_package.description,
        'tasks': tasks,
        'form': form,
        'works': works,
        'tasks_retrieved': tasks_retrieved,
        'zips': zips,
        'formatted_grand_total':  formatted_grand_total
    })
    
def get_task_details(request, task_id):
    task = Task.objects.get(id=task_id)
    return JsonResponse({
        'name': task.name,
        'unit': task.unit,
        'price': task.price,
    })

def budget_delete(request, work_package_id, pk):
    # print("pk: ", pk)
    work = Work.objects.get(pk=pk)
    task_to_erase_id = work.task_id
    task_obj = Task.objects.get(pk=task_to_erase_id)
    workpackage_obj = WorkPackage.objects.get(pk=work_package_id)

    if request.method == 'POST':
        work.delete()
        messages.success(request, 'Work deleted successfully!')

        
        # Updating budget in the database
        works = Work.objects.filter(work_package = work_package_id).select_related('task')
        task_ids = list(Work.objects.filter(work_package = work_package_id).values_list('task_id', flat=False))
        task_ids = [task_id[0] for task_id in task_ids]       

        # calculating the grand total of the chapter:   
        quantities_list = []
        for q in works:
            quantities_list.append(q.quantity)
        
        prices_list = []
        for p in task_ids:
            price = Task.objects.get(id=p).price
            prices_list.append(price)
        
        grand_total = 0
        for i in range(0, len(quantities_list)):
            grand_total += quantities_list[i] * prices_list[i]

        # Storing in the data base, first check if it exist, if exists only update
        wp_budget =WorkpackageTotals(total=grand_total, workpackage_id=work_package_id)
        if WorkpackageTotals.objects.filter(workpackage_id=work_package_id).exists():
            existing_wp_budget = WorkpackageTotals.objects.get(workpackage_id=work_package_id)
            existing_wp_budget.total = grand_total
            existing_wp_budget.save()
        else:
            wp_budget.save()

        return redirect(reverse('budget_create', args=[work_package_id]))
    
    return render(request, 'workpackage/budget_delete.html', {'work': work, 'task_obj': task_obj, 'workpackage_obj': workpackage_obj})


def work_update_database(request):
    if request.method == 'POST':
        # Get the data from the request
        data = json.loads(request.body.decode('utf-8'))

        # Extract the data from the JSON object
        work_id = data.get('work_id')
        field_name = data.get('field_name')
        value = data.get('value')

        # Get the Price object from the database
        work_obj = Work.objects.get(id=work_id)

        # Update the Price object with the new value
        setattr(work_obj, field_name, value)
        work_obj.save()

        # Return a JSON response to indicate success
        return JsonResponse({'message': 'Price updated successfully'})

    else:
        # Return a JSON response to indicate an error
        return JsonResponse({'message': 'Invalid request'}, status=400)
    

def budget_edit(request, work_package_id, pk):
    work = Work.objects.get(pk=pk)
    
    task_to_edit_id = work.task_id
    # print("task to edit id", task_to_edit_id)
    task = Task.objects.get(pk=task_to_edit_id)
    workpackage_obj = WorkPackage.objects.get(pk=work_package_id)
    measurements = Measurement.objects.filter(work=work)
    # print("measurements: ", measurements)

    if not measurements.exists():
        grand_total = Work.objects.get(id=pk).quantity
        
    else:
        grand_total = 0

        for measurement in measurements:
            grand_total += measurement.partial
        work.quantity = grand_total
        work.save()

        
    form = MeasurementForm()
    if request.method == 'POST':
        form = MeasurementForm(request.POST)
        print(form.errors)
        if form.is_valid():
            new_measurement = form.save(commit=False)  # Create a new Measurement instance but don't save it yet
            new_measurement.work = work  # Set the work field
            new_measurement.save()  # Save the new Measurement instance
            measurements = Measurement.objects.filter(work=work)
            # print("measurements: ", measurements)
            messages.success(request, 'Quantity measurement created successfully!')
            return redirect(reverse('budget_edit', args=[work_package_id, pk]))
        else:
            messages.error(request, 'Quantity measurement could not be updated.')
    
    return render(request, 'workpackage/budget_edit.html', {
        'workpackage_obj': workpackage_obj, 
        'pk': pk,
        'task': task,
        'work': work,
        'form': form,
        'measurements': measurements,
        'grand_total': grand_total
        })

def measurement_update(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        measurement_obj = Measurement.objects.get(id=data['id'])

        # print("measurement_obj: ", measurement_obj)
        field_name = data['name']
        field_value = Decimal(data['value'])
        setattr(measurement_obj, field_name, field_value)
        measurement_obj.save()
        # Calculate the updated partial value
        partial_value = measurement_obj.partial
        
        # we update the Grand Total = work.quantity

        work_id = measurement_obj.work_id
        
        work = Work.objects.get(pk=work_id)
        measurements = Measurement.objects.filter(work_id=work_id)
        grand_total = 0
        for measurement in measurements:
            grand_total += measurement.partial
        # print("This is the calculated Grand Total after sending from JS: ", grand_total)
        work.quantity = grand_total
        work.save()

        messages.success(request, 'Field updated successfully!')
        # Return the updated partial value in the JSON response
        return JsonResponse({'message': 'Field updated successfully!', 'partial': partial_value, 'grand_total': grand_total})
    return JsonResponse({'message': 'Invalid request in measurement_update'})


def update_work_quantity(request, work_package_id):
    if request.method == 'POST':
        # print('Received request:', request)
        # print('Request method:', request.method)
        # print('Request data:', request.POST) 
        data = json.loads(request.body)
        quantity = Decimal(data['quantity'])
        work_obj = Work.objects.get(id=work_package_id)
        work_obj.quantity = quantity
        work_obj.save()
        messages.success(request, 'Quantity updated successfully!')
        return JsonResponse({'message': 'Quantity updated successfully!'})
    return JsonResponse({'message': 'Invalid request in update_work_quantity'})

def measurement_delete(request, workpackage_id, work_id, measurement_id):
    measurement = Measurement.objects.get(pk=measurement_id)
    work = Work.objects.get(pk=work_id)
    workpackage = WorkPackage.objects.get(pk=workpackage_id)
    
    if request.method == 'POST':
        measurement.delete()
        messages.success(request, 'Work Package deleted successfully!')
        return redirect(reverse('budget_edit', args=[workpackage_id, work_id]))
    else:
        messages.error(request, 'Work could not be erased.')

    return render(request, 'workpackage/measurement_delete.html', {
        'measurement': measurement, 
        'workpackage': workpackage,
        'work': work
        })



########## WORK PACKAGES####################################################################3    
def workpackage_create(request):
    active_project = ActiveProject.objects.get(user=request.user)
    project_id = active_project.project_id
    project = Project.objects.get(id=project_id)
    project_description = project.description
    
    wps = WorkPackage.objects.all().order_by('name')
   
    if not wps:
        wps = [(None, 'None')]
     
    if request.method == 'POST':
        form = WorkPackageForm(request.POST)
        print(form.errors)
        if 'name' in form.errors:
            messages.error(request, 'Work package with this level already exists, or the data introduced is not valid.')
        if form.is_valid():
            form.save()
            messages.success(request, 'Work Level created successfully!')
            
            wps = WorkPackage.objects.all().order_by('name')

            return render(request, 'workpackage/workpackage_create.html', {
            'form': form,
            'project_description': project_description,
            'project_id': project_id,
            'wps': wps
            })
    else:
        form = WorkPackageForm()
    return render(request, 'workpackage/workpackage_create.html',
            {
            'form': form,
            'project_description': project_description,
            'project_id': project_id,
            'wps': wps
            })

def workpackage_update(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        wp_obj = WorkPackage.objects.get(id=data['id'])
        field_name = data['name']
        field_value = data['value']

        if field_name == 'parent':
            parent_wp = WorkPackage.objects.get(name=field_value)
            setattr(wp_obj, field_name, parent_wp)
        else:
            setattr(wp_obj, field_name, field_value)

        wp_obj.save()
        # messages.success(request, 'Field updated successfully!')
    return JsonResponse({'message': 'Invalid request'})


def workpackage_delete(request, pk):
    wp = WorkPackage.objects.get(pk=pk)
    if request.method == 'POST':
        wp.delete()
        messages.success(request, 'Work Package deleted successfully!')
        return redirect('workpackage_create')  # assuming you have a view for the work package list
    return render(request, 'workpackage/workpackage_delete.html', {'wp': wp})


#################### Copying Works  ##########################################################
# def copy_task_view(request):
#     if request.method == 'POST':
#         form = CopyWorkForm(request.POST)
#         print(form.errors)
#         if form.is_valid():
#             source_workpackage_id = form.cleaned_data['source_workpackage']
#             destination_workpackage_id = form.cleaned_data['destination_workpackage']
#             works_to_copy_ids = request.POST.getlist('works_to_copy')
            
#             for work_to_copy_id in works_to_copy_ids:
#                 copy_task(source_workpackage_id, destination_workpackage_id, work_to_copy_id)

#             messages.success(request, 'Works copied successfully!')
#             return redirect('copy_task')
#     else:
#         form = CopyWorkForm()

#     workpackages = WorkPackage.objects.all()
#     works = Work.objects.all()


#     return render(request, 'workpackage/workpackage_copy.html', {'form': form, 'workpackages': workpackages, 'works': works})
def copy_task_view(request):
    if request.method == 'POST':
        form = CopyWorkPackageForm(request.POST)
        print(form.errors)
        if form.is_valid():
            source_workpackage_id = form.cleaned_data['source_workpackage']
            destination_workpackage_id = form.cleaned_data['destination_workpackage']
            return redirect('work_copy', source_workpackage_id=source_workpackage_id, destination_workpackage_id=destination_workpackage_id)
    else:
        form = CopyWorkPackageForm()
    
    workpackages = WorkPackage.objects.all()

    return render(request, 'workpackage/workpackage_copy.html', {'form': form, 'workpackages': workpackages})

def work_copy_view(request, source_workpackage_id, destination_workpackage_id):
    if request.method == 'POST':
        form = CopyWorkForm(source_workpackage_id, request.POST)
        if form.is_valid():
            works_to_copy_ids = form.cleaned_data['works_to_copy']
            for work_to_copy_id in works_to_copy_ids:
                copy_task(source_workpackage_id, destination_workpackage_id, work_to_copy_id)

            messages.success(request, 'Works copied successfully!')
            return redirect('copy_task')
    else:
        form = CopyWorkForm(source_workpackage_id)
        works = Work.objects.filter(work_package_id=source_workpackage_id)
        work_list = []
        for work in works:
            work_list.append({
                'id': work.id,
                'task_name': work.task.name,
                'quantity': work.quantity
            })

    return render(request, 'workpackage/workpackage_copy_works.html', {'form': form, 'works': work_list})


def copy_task(source_workpackage_id, destination_workpackage_id, work_to_copy_id):
    source_workpackage = WorkPackage.objects.get(id=source_workpackage_id)
    destination_workpackage = WorkPackage.objects.get(id=destination_workpackage_id)
    work_to_copy = Work.objects.get(id=work_to_copy_id)

    # Create a new work with the same attributes as the original work
    new_work = Work(
        task=work_to_copy.task,
        quantity=work_to_copy.quantity,
        work_package=destination_workpackage
    )
    new_work.save()

    # Copy measurements
    for measurement in work_to_copy.measurement_set.all():
        new_measurement = Measurement(
            work=new_work,
            description=measurement.description,
            nr=measurement.nr,
            width=measurement.width,
            length=measurement.length,
            height=measurement.height,
            comment=measurement.comment
        )
        new_measurement.save()
