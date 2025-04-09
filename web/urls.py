from django.urls import path
from . import views

app_name = 'web'

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('entity/<int:pk>/', views.entity_detail, name='entity_detail'),
    path('about/', views.about, name='about'),
]