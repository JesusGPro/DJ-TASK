from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tasks.urls')), 
    path('', include('prices.urls')),
    path('', include('workpackage.urls')),
    path('', include('reports.urls')),
    path('', include('login_budget.urls')),
    # path('workpackages.js', serve, {'document_root': settings.STATIC_ROOT, 'path': 'js/workpackages.js'}),
] 

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)