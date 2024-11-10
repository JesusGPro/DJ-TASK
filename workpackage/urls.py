from django.urls import path
from . import views


urlpatterns = [
    # Budget
    path('budget_assign/', views.budget_assign, name='budget_assign'),
    path('budget_create/<int:work_package_id>/', views.budget_create, name='budget_create'),
    path('get-task-details/<str:task_id>/', views.get_task_details, name='get_task_details'),
    path('budget_create/<int:work_package_id>/delete/<pk>/', views.budget_delete, name='budget_delete'),
    path('updatework/', views.work_update_database, name='work_update_database'),
    path('budget_create/<int:work_package_id>/edit/<pk>/', views.budget_edit, name='budget_edit'),
    path('measurement_update/', views.measurement_update, name='measurement_update'),
    path('budget_create/<int:work_package_id>/update_quantity/', views.update_work_quantity, name='update_work_quantity'),
    path('measurement_delete/<int:workpackage_id>/<int:work_id>/<int:measurement_id>', views.measurement_delete, name='measurement_delete'),
    # WorkPackages
    path('workpackage_create/', views.workpackage_create, name='workpackage_create'),
    path('workpackage_update/', views.workpackage_update, name='workpackage_update'),
    path('workpackages/<pk>/delete/', views.workpackage_delete, name='workpackage_delete'),

    # Copy task in WorkPackages
    path('copy_task/', views.copy_task_view, name='copy_task'),
    path('copy-task/<int:source_workpackage_id>/<int:destination_workpackage_id>/', views.work_copy_view, name='work_copy'),
]