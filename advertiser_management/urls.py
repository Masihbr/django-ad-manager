from django.urls import path
from . import views
from .views import Clicker, CreateAdPage, HomePageView, AdPageView, ReportPageView, AdListAPIView

urlpatterns = [
    path('', HomePageView.as_view(), name='ads'),
    path('click/<int:pk>/', Clicker.as_view(), name='clicker'),
    path('ad/<int:pk>/', AdPageView.as_view(), name='ad'),
    path('create_ad/', CreateAdPage.as_view(), name='create_ad'),
    path('report/', ReportPageView.as_view(), name='report'),
    # path('ad_list/', views.ad_list, name='ad_list'),
    path('ad_list/',AdListAPIView.as_view() , name='ad_list'),
    path('ad_each/<int:pk>/', views.ad, name='ad_each'),
]
