# urls.py
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cohorts/', include('cohorts_and_students.urls')),
]