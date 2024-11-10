from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # Project
    path('project_create/', views.project_create, name='project_create'),
    path('project_select/', views.project_select, name='project_select'),
    path('projects/<int:project_id>/', views.project_detail, name='project_detail'),
    path('projects/<pk>/edit/', views.project_edit, name='project_edit'),
    path('projects/<pk>/delete/', views.project_delete, name='project_delete'),
    # Currency
    path('currency_create/', views.currency_create, name='currency_create'),
    path('currency_edit/', views.currency_edit, name='currency_edit'),
]