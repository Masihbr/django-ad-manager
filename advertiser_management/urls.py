from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (Clicker, CreateAdPage, HomePageView, AdPageView, ReportPageView, AdViewset, AdvertiserViewset,
                    ClickViewset, ViewViewset)

router = DefaultRouter()
router.register(r'ad_list', AdViewset, basename='ad_list')
router.register(r'advertiser_list', AdvertiserViewset, basename='advertiser_list')
router.register(r'click_list', ClickViewset, basename='click_list')
router.register(r'view_list', ViewViewset, basename='view_list')

urlpatterns = [
    path('', HomePageView.as_view(), name='ads'),
    path('click/<int:pk>/', Clicker.as_view(), name='clicker'),
    path('ad/<int:pk>/', AdPageView.as_view(), name='ad'),
    path('create_ad/', CreateAdPage.as_view(), name='create_ad'),
    path('report/', ReportPageView.as_view(), name='report'),
    path('viewset/',include(router.urls)),
    path('viewset/<int:pk>/',include(router.urls)),
]
