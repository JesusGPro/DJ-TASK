from django.shortcuts import render, redirect, get_object_or_404
from .forms import PriceForm, TaskSelectionForm, TaskGroupForm, TaskForm, TaskInstanceForm, TaskSubGroupForm, TaskSelectionQuantityForm
from .models import Price, TaskSelection, TaskGroup, Task, TaskInstance, TaskSubGroup, TaskSelectionQuantity
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from decimal import Decimal
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.db.models import Sum
from django.http import QueryDict, HttpResponse
from django.forms.formsets import formset_factory
from decimal import Decimal
from django.http import JsonResponse
import json
from django.db import transaction
from django.template.context_processors import csrf
from django.urls import reverse

def home(request):
    return render(request, 'tasks/home.html')

def price_list(request):
    prices = Price.objects.all()
    return render(request, 'tasks/price_list.html', {'prices': prices})

def price_create(request):
    if request.method == 'POST':
        form = PriceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('price_list')
        else:
            print(form.errors)  # Print the form errors
    else:
        form = PriceForm()
    return render(request, 'tasks/price_create.html', {'form': form})

def edit_record(request, pk):
    record = Price.objects.get(pk=pk)
    if request.method == 'POST':
        form = PriceForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('price_list')
    else:
        form = PriceForm(instance=record)
    return render(request, 'tasks/record_edit.html', {'form': form, 'record': record, 'pk': pk})

def delete_records(request):
    if request.method == 'POST':
        record_keys = request.POST.getlist('record_keys')
        print(f"Record keys: {record_keys}")  
        records_to_delete = Price.objects.filter(id__in=record_keys)
        print(f"Records to delete: {records_to_delete}")
        deleted_count, _ = records_to_delete.delete()
        if deleted_count > 0:
            messages.success(request, 'Price deleted successfully')
        else:
            messages.error(request, 'No records deleted')
        return redirect('price_list')
    else:
        form = PriceForm()
    return render(request, 'tasks/price_list.html', {'form': form})

def select_drawer_view(request):
    drawers = drawers = list(TaskGroup.objects.all()) + list(TaskSubGroup.objects.all()) + list(Task.objects.all()) + list(TaskInstance.objects.all())
    if request.method == 'POST':
        selected_drawer_id = request.POST.get('drawer')
        return redirect('task_selection', selected_drawer_id)
    return render(request, 'tasks/select_drawer.html', {'drawers': drawers})


def task_selection_view(request, selected_drawer_id=None):
    print("selected_drawer_id:", selected_drawer_id)

    if selected_drawer_id is None:
        selected_drawer_id = request.GET.get('selected_drawer_id', request.POST.get('selected_drawer_id'))
        print("selected_drawer_id from POST:", selected_drawer_id)

    drawers = list(TaskGroup.objects.all()) + list(TaskSubGroup.objects.all()) + list(Task.objects.all()) + list(TaskInstance.objects.all())

    if selected_drawer_id:
        selected_drawer = drawers[int(selected_drawer_id) - 1]
    else:
        selected_drawer = drawers[0]

    selections = TaskSelection.objects.filter(drawer_object_id=selected_drawer.id)

    total_sum = 0
    partial_sums = []
    for selection in selections:
        price = selection.price.price
        quantity = selection.quantity
        currency = selection.price.currency

        # Convert the price to USD
        if currency == 'EUR':
            price_in_usd = price * Decimal('1.10')
        elif currency == 'SAR':
            price_in_usd = price * (Decimal('1') / Decimal('3.75'))
        else:  # assume USD
            price_in_usd = price

        partial_sum = price_in_usd * quantity
        partial_sums.append(partial_sum)
        total_sum += partial_sum

    partial_sums_formatted = [format("{:,.2f}".format(x)) for x in partial_sums]
    total_sum_formatted = format("{:,.2f}".format(total_sum))

    form = TaskSelectionForm(request.POST or None)
    prices = Price.objects.all()

    if request.method == 'POST':
        form.fields['content_type'].initial = ContentType.objects.get_for_model(selected_drawer.__class__).id
        price_code = request.POST.get('prices')
        if price_code:
            price_obj = Price.objects.get(code=price_code)

            mutable_data = QueryDict(mutable=True)
            mutable_data['csrfmiddlewaretoken'] = request.POST.get('csrfmiddlewaretoken')
            mutable_data['price'] = price_obj.id
            mutable_data['quantity']= request.POST.get('quantity')
            mutable_data['content_type'] = ContentType.objects.get(id=selected_drawer_id)
            mutable_data['drawer_content_type'] = ContentType.objects.get_for_model(selected_drawer.__class__).id
            mutable_data['drawer_object_id'] = selected_drawer.id
            mutable_data['selected_drawer_id']= request.POST.get('selected_drawer_id')

            print(mutable_data)

            new_form = form.__class__(mutable_data)

            print(new_form.errors)

        if new_form.is_valid():
            task_selection = new_form.save(commit=False)
            task_selection.drawer_content_type_id = ContentType.objects.get_for_model(selected_drawer.__class__).id
            task_selection.drawer_object_id = selected_drawer.id
            task_selection.save()
            return redirect(request.path)

    return render(request, 'tasks/task_selection.html', {
        'form': form,
        'prices': prices,
        'selections_with_sums': zip(selections, partial_sums_formatted),
        'total_sum': total_sum_formatted,
        'drawers': drawers,
        'selected_drawer': selected_drawer,
        'selected_drawer_id': selected_drawer_id,
    })

def edit_task_selection(request, selected_id):
    # Get the TaskSelection object with the given ID
    task_selection = get_object_or_404(TaskSelection, pk=selected_id)

    # Create a form with initial values
    form = TaskSelectionForm(request.POST or None, instance=task_selection)

    # Get all drawers
    drawers = list(TaskGroup.objects.all()) + list(TaskSubGroup.objects.all()) + list(Task.objects.all()) + list(TaskInstance.objects.all())
    price_choices = Price.objects.all()

    if request.method == 'POST' and form.is_valid():
        print("We are in edit_task_selection")
        # Update the drawer field
        selected_price = form.cleaned_data['price']
        task_selection.price = selected_price
        task_selection.save()

        # Print errors if any (for debugging)
        print(form.errors)

        # Print saved object (for debugging)
        print("Saved task selection:", task_selection)

        # Redirect to the desired success page
        return redirect('select_drawer')  # Replace with your success URL pattern
    else:
        print("Form is invalid or request method is not POST")
        print(form.errors)  # Print form errors for debugging

    # Render the template with context variables
    return render(request, 'tasks/edit_task_selection.html', {
        'task_selection': task_selection,
        'form': form,
        'drawers': drawers,
        'price_choices': price_choices,
    })


def task_selection_delete(request, pk):
    selection = get_object_or_404(TaskSelection, pk=pk)
    selected_drawer_id = selection.drawer_object_id

    if request.method == 'POST':
        if selection.delete():
            messages.success(request, 'Price deleted successfully')
        else:
            messages.error(request, 'No records deleted')
        return redirect(reverse('task_selection', args=[selected_drawer_id])) 
    return render(request, 'tasks/task_selection_delete.html', {'pk': pk, 'selected_drawer_id': selection.drawer_object_id})


###################################################################################################
# TaskGroup views
class TaskGroupCreateView(CreateView):
    model = TaskGroup
    form_class = TaskGroupForm
    template_name = 'tasks/taskgroup_create.html'
    success_url = '/taskgroups/'

class TaskGroupListView(ListView):
    model = TaskGroup
    template_name = 'tasks/taskgroup_list.html'
    ordering = ['name']

class TaskGroupUpdateView(UpdateView):
    model = TaskGroup
    form_class = TaskGroupForm
    template_name = 'tasks/taskgroup_update.html'
    success_url = '/taskgroups/'

class TaskGroupDeleteView(DeleteView):
    model = TaskGroup
    template_name = 'tasks/taskgroup_delete.html'
    success_url = '/taskgroups/'

# TaskSubGroup views
class CreateSubGroupView(CreateView):
    model = TaskSubGroup
    form_class = TaskSubGroupForm
    template_name = 'tasks/subgroup_create.html'
    success_message = 'Task subgroup created successfully!'
    success_url = '/subgroups/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parent_groups'] = TaskGroup.objects.all()
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, self.success_message)
        return redirect('subgroup_list')

class SubGroupListView(ListView):
    model = TaskSubGroup
    template_name = 'tasks/subgroup_list.html'
    

class UpdateSubGroupView(UpdateView):
    model = TaskSubGroup
    form_class = TaskSubGroupForm
    template_name = 'tasks/subgroup_update.html'
    success_message = 'Task subgroup updated successfully!'
    pk_url_kwarg = 'pk'
    success_url = '/subgroups/'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, self.success_message)
        return redirect('subgroup_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subgroup'] = self.object  # Pass the subgroup object to the template
        context['parent_groups'] = TaskSubGroup.objects.all()
        return context

class DeleteSubGroupView(DeleteView):
    model = TaskSubGroup
    template_name = 'tasks/subgroup_delete.html'
    success_message = 'Task subgroup deleted successfully!'
    pk_url_kwarg = 'pk'  # Add this line
    success_url = '/subgroups/'

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        messages.success(self.request, self.success_message)
        return redirect('subgroup_list')

# Task views
class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_create.html'
    success_message = 'Task created successfully!'
    success_url = '/task_create/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        context['subgroups'] = TaskSubGroup.objects.all()
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, self.success_message)
        return redirect('task_create')

class TaskListView(ListView):
    model = Task
    template_name = 'task_list.html'
    ordering = ['name']

    def form_valid(self, form):
        form.save()
        return redirect(self.success_url)

class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_update.html'
    success_url = '/tasks/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['form'] = self.form_class()
        context['subgroups'] = TaskSubGroup.objects.all()
        return context


class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'tasks/task_delete.html'
    success_url = '/tasks/'

# TaskInstance views
class TaskInstanceCreateView(CreateView):
    model = TaskInstance
    form_class = TaskInstanceForm
    success_message = 'Task instance created successfully!'
    template_name = 'tasks/taskinstance_create.html'
    success_url = '/taskinstances/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        context['tasks'] = Task.objects.all()
        return context

    def form_valid(self, form):
        if form.is_valid():
            form.save()
            messages.success(self.request, self.success_message)
            return redirect('taskinstance_list')
        else:
            messages.error(self.request, 'Form is not valid')
            return self.render_to_response(self.get_context_data(form=form))
    

class TaskInstanceListView(ListView):
    model = TaskInstance
    template_name = 'tasks/taskinstance_list.html'
    success_url = '/taskinstances/'
    ordering = ['name']

    def form_valid(self, form):
        form.save()
        return redirect(self.success_url)

class TaskInstanceUpdateView(UpdateView):
    model = TaskInstance
    form_class = TaskInstanceForm
    template_name = 'tasks/taskinstance_update.html'
    success_url = '/taskinstances/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['obj'] = self.object
        context['tasks'] = Task.objects.all()
        return context
    
    def post(self, request, *args, **kwargs):
        print("Post method called")
        print(request.POST)
        instance = self.get_object()  # Get the instance from the database
        form = self.form_class(request.POST, instance=instance)  # Pass the instance to the form
        if form.is_valid():
            form.save()  # Save the updated instance
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class TaskInstanceDeleteView(DeleteView):
    model = TaskInstance
    template_name = 'tasks/taskinstance_delete.html'
    success_url = '/taskinstances/'


###########################################################################################
def edit_task_selection_quantity(request, task_selection_id):
    quantities = TaskSelectionQuantity.objects.filter(task_id=task_selection_id).order_by('-id')
    task_selection = TaskSelection.objects.get(pk=task_selection_id)
    print("We are before the post")
    total_quantity = quantities.aggregate(Sum('quantity')).get('quantity__sum', 0)
    print("total quantities before the POST", total_quantity)

    if request.method == 'POST':
        form = TaskSelectionQuantityForm(request.POST, initial={'task': task_selection_id})
        print(form.errors)
        print("We are before the validation")
        if form.is_valid():
            new_quantity = float(request.POST.get('nr')) * float(request.POST.get('width')) * float(request.POST.get('length')) * float(request.POST.get('height'))
            new_quantity = Decimal(new_quantity)
            # Create a new instance of TaskSelectionQuantity
            denomination = request.POST.get('denomination')
            nr = request.POST.get('nr')
            width = request.POST.get('width')
            length = request.POST.get('length')
            height = request.POST.get('height')
            notes = request.POST.get('notes')
            TaskSelectionQuantity(task=task_selection, quantity=new_quantity, denomination=denomination, nr=nr, width=width, length=length, height=height).save()
            print("This should be the new quantity: ", Decimal(new_quantity))
            # total_quantity = quantities.aggregate(Sum('quantity')).get('quantity__sum', 0) + Decimal(new_quantity)
            total_quantity = Decimal(0)
            for quantity in quantities:
                total_quantity += quantity.quantity
                print("quantity from data base: ", total_quantity)
            # total_quantity += new_quantity
            print(total_quantity)
            task_selection.quantity = total_quantity
            task_selection.save()
            return redirect('edit_task_selection_quantity', task_selection_id=task_selection_id)
            
    else:
        form = TaskSelectionQuantityForm(initial={'task': task_selection_id})

    return render(request, 'tasks/edit_task_selection_quantity.html', {'pk': task_selection_id, 'form': form, 'quantities': quantities, 'task_selection': task_selection.price, 'selected_drawer_id': task_selection.drawer_object_id})






def delete_quantity(request, pk):
    quantity = get_object_or_404(TaskSelectionQuantity, pk=pk)
    quantity.delete()
    return redirect(request.META.get('HTTP_REFERER'))

def update_quantity(request):
    pk = request.POST.get('pk')
    value = request.POST.get('value')
    quantity = get_object_or_404(TaskSelectionQuantity, pk=pk)
    quantity.quantity = value
    quantity.save()
    return JsonResponse({'value': value})


def update_database(request, task_selection_id):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        # for example: data= {'id': '42', 'field_name': 'nr', 'value': '10', 'quantity_value': 0.6}
        print('data: ', data)
        id = data.get('id')
        field_name = data.get('field_name')
        new_value = data.get('value')
        new_quantity = data.get('quantity_value')
        grand_total = data.get('grand_total')

        if not all([id, field_name, new_value, new_quantity, grand_total]):
            return JsonResponse({'error': 'No updates provided'}, status=400)

        my_object = TaskSelectionQuantity.objects.get(id=id)
        print("We are in update_database: my_object", my_object)

        # Extract the TaskSelection ID from the URL
        # task_selection_id = 31
        print("The task_selection id: ", task_selection_id)

        # Retrieve the associated TaskSelection object
        task_selection = TaskSelection.objects.get(id=task_selection_id)
        print("task_selection object: ", task_selection)

        # Retrieve the associated TaskSelection object
        task_selection.quantity = grand_total
        task_selection.save()

        
        if field_name == 'nr' or 'notes':
            setattr(my_object, field_name, new_value)
        else:
            clean_value = float(new_value.replace(',', ''))
            setattr(my_object, field_name, clean_value)
        
        my_object.quantity = new_quantity
        my_object.save()

        print(f"Updated {', '.join(data.keys())} to {', '.join(map(str, data.values()))} for object {id}")
        return JsonResponse({'message': f"Updated {', '.join(data.keys())} to {', '.join(map(str, data.values()))} for object {id}"})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

def update_task_selection_list(request):
    tasks = Task.objects.all()
    for task in tasks:
        total_quantity = TaskSelectionQuantity.objects.filter(task=task).aggregate(total_quantity=Sum('quantity'))['total_quantity']
        task.total_quantity = total_quantity
        task.save()
    return HttpResponse("Task selection list updated successfully!")