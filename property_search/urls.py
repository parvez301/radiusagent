from django.urls import path
from property_search import views

urlpatterns = [
    path('', views.property_search),
]