from django.urls import path
from . import views
from .views import Clicker, CreateAdPage, HomePageView, AdPageView

urlpatterns = [
    path('', HomePageView.as_view(), name='ads'),
    path('click/<int:pk>/', Clicker.as_view(), name='clicker'),
    path('ad/<int:pk>/', AdPageView.as_view(), name='ad'),
    path('create_ad/', CreateAdPage.as_view(), name='create_ad')
]
