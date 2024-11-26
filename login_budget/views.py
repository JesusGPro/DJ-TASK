from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
from django.contrib import messages
from tasks.models import Project, ActiveProject

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                # Code to check if there is an active project
                # Fetch user projects and active projects
                user_projects = Project.objects.filter(tenant=user)
                active_projects = ActiveProject.objects.filter(user=user)
                ########################################################

                # Store the project information in the session
                request.session['user_projects_count'] = user_projects.count()
                request.session['active_projects_count'] = active_projects.count()
                return redirect(reverse('home'))
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login_budget/login.html", context={"form":form})

def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect(reverse('home'))
