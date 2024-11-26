from django.urls import path
from . import views

urlpatterns = [
    # components
    path('projects/<int:project_id>/prices_create/', views.prices_create, name='prices_create'),
    path('projects/<int:project_id>/prices/<int:pk>/delete/', views.prices_delete, name='prices_delete'),
    path('updateprice/', views.prices_update_database, name='prices_update_database'),
    path('trial/', views.trial, name='trial'),
    # adding one to the last code
    path('prices/get_last_code/<int:project_id>/', views.get_last_code, name='get_last_code'),
    path('task_component_quantity_update/', views.task_component_quantity_update, name='task_component_quantity_update'),

    # tasks
    path('tasks/<int:project_id>/create/', views.task_create, name='task_create'),
    path('tasks/<int:project_id>/task/<int:pk>/delete/', views.tasks_delete, name='tasks_delete'),
    path('tasks/<int:project_id>/task/<int:pk>/detail/', views.tasks_detail, name='tasks_detail'),
    path('tasks/<int:project_id>/task/<int:pk>/add_component/', views.tasks_add_component, name='tasks_add_component'),
    path('tasks/<int:project_id>/task/<int:pk>/detail/<int:comp_id>', views.tasks_comp_delete, name='tasks_comp_delete'),
    path('task_name_update/', views.task_name_update, name='task_name_update'),
    
]