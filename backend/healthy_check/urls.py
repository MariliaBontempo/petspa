from django.urls import path
from . import views

urlpatterns=[
    path('api/frontend_backend_heakth/',
         views.frontend_backend_health,
         name='frontend_backend_health',
    ),
]
