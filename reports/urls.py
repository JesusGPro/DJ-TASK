from django.urls import path
from . import views

urlpatterns = [
    path('work-package-assign/', views.work_package_assign, name='work_package_assign'),
    path('work-package-report/<int:work_package_id>/', views.work_package_report, name='work_package_report'),

    # Workpackage Total
    path('work-package-report-total-index/', views.work_package_total_pick, name='work_package_report_total_pick'),
    path('work-package-report-total/', views.work_package_report_total, name='work_package_report_total'),
    path('work-package-report-total-pdf/', views.work_package_report_total_pdf, name='work_package_report_total_pdf'),
    path('work-package-report-total-csv/', views.work_package_report_total_csv, name='work_package_report_total_csv'),
    # Totals with measurements
    path('work-package-report-measurement-total/', views.work_package_report_measurement_total, name='work_package_report_measurement_total'),
    path('work-package-report-measurement-total-pdf/', views.work_package_report_measurement_total_pdf, name='work_package_report_measurement_total_pdf'),
    path('work-package-report-measurement-total-csv/', views.work_package_report_measurement_total_csv, name='work_package_report_measurement_total_csv'),
    path('work-package-report-measurement-total-excel/', views.work_package_report_measurement_total_excel, name='work_package_report_measurement_total_excel'),
    # Workpackage Total Summary
    path('work-package-report-total-summary/', views.work_package_report_total_summary, name='work_package_report_total_summary'),
    path('work-package-report-total-summary-pdf/', views.work_package_report_total_summary_pdf, name='work_package_report_total_summary_pdf'),
    path('work-package-report-total-summary-csv/', views.work_package_report_total_summary_csv, name='work_package_report_total_summary_csv'),

    # Workpackages
    path('work-package-pdf/<int:work_package_id>/', views.work_package_pdf, name='work_package_pdf'),
    path('work-package-csv/<int:work_package_id>/', views.work_package_csv, name='work_package_csv'),

    # components
    path('component_report/', views.component_report, name='component_report'),
    path('component_report_pdf/', views.component_report_pdf, name='component_report_pdf'),
    path('component_report_csv/', views.component_report_csv, name='component_report_csv'),

    # tasks
    path('task_report/', views.task_report, name='task_report'),
    path('task_report_pdf/', views.task_report_pdf, name='task_report_pdf'),
    path('task_report_csv/', views.task_report_csv, name='task_report_csv'),
    path('task_report_weight/', views.task_report_weight, name='task_report_weight'),
    path('task_report_weight_pdf/', views.task_report_weight_pdf, name='task_report_weight_pdf'),
    path('task_report_weight_csv/', views.task_report_weight_csv, name='task_report_weight_csv'),
    path('task_components_report/', views.task_components_report, name='task_components_report'),
    path('task_components_report_pdf/', views.task_components_report_pdf, name='task_components_report_pdf'),
    path('task_components_report_csv/', views.task_components_report_csv, name='task_components_report_csv'),
    path('task_components_report_excel/', views.task_components_report_excel, name='task_components_report_excel'),

    # workpackages with measurement
    path('work_package_report_measurement/<int:work_package_id>/', views.work_package_report_measurement, name='work_package_report_measurement'),
    path('work_package_report_measurement_pdf/<int:work_package_id>/', views.work_package_report_measurement_pdf, name='work_package_report_measurement_pdf'),
    path('work_package_report_measurement_csv/<int:work_package_id>/', views.work_package_report_measurement_csv, name='work_package_report_measurement_csv'),
    path('work_package_report_measurement_xlsx/<int:work_package_id>/', views.work_package_report_measurement_xlsx, name='work_package_report_measurement_xlsx'),

    # workpackages with children
    path('work-packagechildren-assign/', views.work_packagechildren_assign, name='work_packagechildren_assign'),
    path('work-packagechildren-report/<int:work_package_id>/', views.work_packagechildren_report, name='work_packagechildren_report'),
    path('work-packagechildren-report-pdf/<int:work_package_id>/', views.work_packagechildren_report_pdf, name='work_packagechildren_report_pdf'),
    path('work-packagechildren-report-excel/<int:work_package_id>/', views.work_packagechildren_report_excel, name='work_packagechildren_report_excel'),
]