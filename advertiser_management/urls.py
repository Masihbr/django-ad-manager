from django.urls import path
from . import views
from .views import Clicker

urlpatterns = [
    path('', views.home, name='ads'),
    path('click/<int:pk>/', Clicker.as_view(), name='clicker'),
    path('ad/<int:pk>/', views.ad, name='ad'),
    path('create_ad/', views.create_ad, name='create_ad')
]
