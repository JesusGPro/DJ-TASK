from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Project, ActiveProject, Currency
from .forms import ProjectForm, CurrencyForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
import markdown
import os

def base_view(request):
    # Get all projects created by the user
    user_projects = Project.objects.filter(tenant=request.user)
    # Get active projects for the user
    active_projects = ActiveProject.objects.filter(user=request.user)

    context = {
        'user_projects': user_projects,
        'active_projects': active_projects,
    }
    return render(request, 'base.html', context)


def home(request):
    if request.user.is_authenticated:
        projects = Project.objects.filter(tenant=request.user)
        return render(request, 'tasks/home.html', {'projects': projects})
    else:
        return render(request, 'tasks/home.html', {})

def project_create(request, project_id=None):
    if not request.user.is_authenticated:
        return HttpResponse("You must be logged in to create a Project.")
    # if project_id is None:
    #     return HttpResponse("You must choose a project to create a price.")
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        print(form.errors)
        if form.is_valid():
            project = form.save(commit=False)
            project.tenant = request.user
            form.save()
            messages.info(request, f"Project created successfully.")
            return redirect('home')
        else:
            messages.error(request,"Fail to create the Project.")
    else:
        form = ProjectForm()
    return render(request, 'tasks/project_create.html', {'form': form})

def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated successfully')
            return redirect('project_detail', project_id=pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'tasks/project_edit.html', {'form': form})

def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        # Check if there are any remaining projects for the user
        user_projects = Project.objects.filter(tenant=request.user)
        
        if not user_projects.exists():
            # Clear the session if no projects are left
            request.session.pop('selected_project_id', None)
            messages.info(request, "All projects have been deleted. Please create a new project.")
        return redirect('home')
    return render(request, 'tasks/project_delete.html', {'project': project, 'pk': pk})

def project_select(request):
    if not request.user.is_authenticated:
        return redirect('home')
    projects = Project.objects.filter(tenant=request.user)
    if request.method == 'POST':
        selected_project_id = request.POST.get('project_id')
        print("Selected project ID:", selected_project_id)
        request.session['selected_project_id'] = selected_project_id
        return redirect('project_detail', project_id=selected_project_id)
    return render(request, 'tasks/project_select.html', {'projects': projects})

def project_detail(request, project_id):
    project = Project.objects.get(id=project_id)
    ActiveProject.objects.update_or_create(user=request.user, project=project)
    request.session['active_project_id'] = project_id

    return render(request, 'tasks/project_detail.html', {'project': project})

def projects_get_users(request):
    projects = Project.objects.filter(tenant=request.user)
    return render(request, 'tasks/project_list.html', {'projects': projects})

def currency_create(request):
    if Currency.objects.exists():  # Check if a currency instance already exists
        return redirect('currency_edit')
    else:
        form = CurrencyForm()
        if request.method == 'POST':
            form = CurrencyForm(request.POST)  # Bind the form to the request data
            if form.is_valid():  # Validate the form data
                form.save()
                return redirect('home')
        return render(request, 'tasks/currency_create.html')

def currency_edit(request):
    currency_instance = Currency.objects.first()  # Assuming there's only one instance
    print(currency_instance)
    if request.method == 'POST':
        form = CurrencyForm(request.POST, instance=currency_instance)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CurrencyForm(instance=currency_instance)
    return render(request, 'tasks/currency_edit.html', {'form': form, 'currency': currency_instance})


######################################### Instructions with Markdown ##########################################
def markdown_view(request):
    # Path to your markdown file
    md_file_path = os.path.join(os.path.dirname(__file__), 'instructions', 'instructions.md')
    
    # Read the markdown file
    with open(md_file_path, 'r') as md_file:
        content = md_file.read()
    
    # Convert markdown to HTML
    html_content = markdown.markdown(content)
    
    return render(request, 'tasks/markdown.html', {'content': html_content})