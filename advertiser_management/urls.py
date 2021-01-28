from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='ads'),
    path('click/<int:ad_id>', views.click, name='click')
]