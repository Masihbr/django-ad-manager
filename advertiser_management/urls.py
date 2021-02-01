from django.urls import path
from . import views
from .views import Clicker, CreateAd, HomePageView

urlpatterns = [
    path('', HomePageView.as_view(), name='ads'),
    path('click/<int:pk>/', Clicker.as_view(), name='clicker'),
    path('ad/<int:pk>/', views.ad, name='ad'),
    path('create_ad/', CreateAd.as_view(), name='create_ad')
]
