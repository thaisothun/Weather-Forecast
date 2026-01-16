from . import views
from django.urls import path

urlpatterns= [
    path('details_forecast', views.current_city, name='current_city'),
    path('', views.home, name='home'),
    
]