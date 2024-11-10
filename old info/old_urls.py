from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('prices/', views.price_list, name='price_list'),
    path('prices/create/', views.price_create, name='price_create'),
    path('record/<pk>/edit/', views.edit_record, name='edit_record'),
    path('records/delete/', views.delete_records, name='delete_records'),
    path('select_drawer/', views.select_drawer_view, name='select_drawer'),
    path('task_selection/<int:selected_drawer_id>/', views.task_selection_view, name='task_selection'),
    path('edit_task_selection/<int:selected_id>/', views.edit_task_selection, name='edit_task_selection'),
    path('task_selection/<int:pk>/delete/', views.task_selection_delete, name='task_selection_delete'),
    path('update_database/<int:task_selection_id>/', views.update_database, name='update_database'),
    

    # editing quantities
    path('task_selection/<int:task_selection_id>/edit_quantity/', views.edit_task_selection_quantity, name='edit_task_selection_quantity'),
    path('delete_quantity/<pk>/', views.delete_quantity, name='delete_quantity'),
    path('update_quantity/', views.update_quantity, name='update_quantity'),
    
    # TaskGroup URLs
    path('taskgroups/', views.TaskGroupListView.as_view(), name='taskgroup_list'),
    path('taskgroups/create/', views.TaskGroupCreateView.as_view(), name='taskgroup_create'),
    path('taskgroups/<pk>/update/', views.TaskGroupUpdateView.as_view(), name='taskgroup_update'),
    path('taskgroups/<pk>/delete/', views.TaskGroupDeleteView.as_view(), name='taskgroup_delete'),

    # TaskSubGroup URLs
    path('subgroups/', views.SubGroupListView.as_view(), name='subgroup_list'),
    path('subgroups/create/', views.CreateSubGroupView.as_view(), name='subgroup_create'),
    path('subgroups/<pk>/update/', views.UpdateSubGroupView.as_view(), name='subgroup_update'),
    path('subgroups/<pk>/delete/', views.DeleteSubGroupView.as_view(), name='subgroup_delete'),
    
    # Task URLs
    path('tasks/', views.TaskListView.as_view(), name='task_list'),
    path('tasks/create/', views.TaskCreateView.as_view(), name='task_create'),
    path('tasks/<pk>/update/', views.TaskUpdateView.as_view(), name='task_update'),
    path('tasks/<pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),

    # TaskInstance URLs
    path('taskinstances/', views.TaskInstanceListView.as_view(), name='taskinstance_list'),
    path('taskinstances/create/', views.TaskInstanceCreateView.as_view(), name='taskinstance_create'),
    path('taskinstances/<pk>/update/', views.TaskInstanceUpdateView.as_view(), name='taskinstance_update'),
    path('taskinstances/<pk>/delete/', views.TaskInstanceDeleteView.as_view(), name='taskinstance_delete'),
]