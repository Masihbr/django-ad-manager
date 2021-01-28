from django.urls import path
from . import views
from .views import Clicker

urlpatterns = [
    path('', views.home, name='ads'),
    path('click/<int:ad_id>', Clicker.as_view(), name='clicker'),
    path('ad/<int:ad_id>', views.ad, name='ad')
]
