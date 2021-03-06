from collections import OrderedDict

from django.db.models.functions import Trunc, TruncHour, ExtractHour
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.db.models import Count, DateTimeField
from rest_framework import status, generics, mixins, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import create_ad_form
from .models import Advertiser, Ad, Click, View
from django.shortcuts import get_object_or_404
from django.views.generic.base import RedirectView, TemplateView

from .serializers import AdSerializer, AdvertiserSerializer, ClickSerializer, ViewSerializer

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly


class AdViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

    serializer_class = AdSerializer
    queryset = Ad.objects.all()


class AdvertiserViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

    serializer_class = AdvertiserSerializer
    queryset = Advertiser.objects.all()


class ClickViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated & IsAdminUser]

    serializer_class = ClickSerializer
    queryset = Click.objects.all()


class ViewViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated & IsAdminUser]

    serializer_class = ViewSerializer
    queryset = View.objects.all()


class HomePageView(TemplateView):
    template_name = 'advertiser_management/ads.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['advertisers'] = Advertiser.objects.all()
        return context


class Clicker(RedirectView):
    pattern_name = 'ad'

    def get_redirect_url(self, *args, **kwargs):
        ad = get_object_or_404(Ad, pk=kwargs['pk'])
        return super().get_redirect_url(*args, **kwargs)


class AdPageView(TemplateView):
    template_name = 'advertiser_management/ad.html'
    click_per_hour = Ad.objects.annotate(
        clicked=Trunc('click__time', 'hour', output_field=DateTimeField())
    ).values('clicked').annotate(clicks=Count('click'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ad = get_object_or_404(Ad, pk=kwargs['pk'])
        context['ad'] = ad
        return context


class CreateAdPage(CreateView):
    model = Ad
    form_class = create_ad_form
    template_name = 'advertiser_management/ad_form.html'


class ReportPageView(TemplateView):
    template_name = "advertiser_management/report.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        clicks_views_sum_list = self.get_clicks_views_sum_list()
        clicks_per_views_list = self.get_clicks_per_view_list()
        avg_click_view_diff_list = self.get_avg_click_view_diff_list()
        context = {
            'avg_click_view_diff_list': avg_click_view_diff_list,
            'clicks_per_views_list': clicks_per_views_list,
            'clicks_views_sum_list': clicks_views_sum_list,
            'ads_list': Ad.objects.all()
        }
        return context

    def get_clicks_per_view_list(self):
        clicks_per_views_list = {}
        for ad in Ad.objects.all():
            list = {}
            clicks_per_hour = self.get_clicks_per_hour(ad)
            views_per_hour = self.get_views_per_hour(ad)
            for view in views_per_hour:
                list[view['hour']] = view['views']
            for click in clicks_per_hour:
                if list.keys().__contains__(click['hour']):
                    list[click['hour']] = click['clicks'] / list[click['hour']]
                else:
                    list[click['hour']] = 0
            clicks_per_views_list[ad] = sorted(list.items(), reverse=True, key=lambda t: t[1])
        return clicks_per_views_list

    def get_clicks_views_sum_list(self):
        clicks_views_sum_list = {}
        for ad in Ad.objects.all():
            list = {}
            clicks_per_hour = self.get_clicks_per_hour(ad)
            views_per_hour = self.get_views_per_hour(ad)
            for click in clicks_per_hour:
                list[click['hour']] = click['clicks']
            for view in views_per_hour:
                if list.keys().__contains__(view['hour']):
                    list[view['hour']] += view['views']
                else:
                    list[view['hour']] = view['views']
            clicks_views_sum_list[ad] = sorted(list.items(), key=lambda t: t[0])
        return clicks_views_sum_list

    def get_avg_click_view_diff_list(self):
        avg_click_view_diff_list = {}
        for ad in Ad.objects.all():
            views = View.objects.filter(ad=ad).order_by('time')
            clicks = Click.objects.filter(ad=ad).order_by('time')
            for click in clicks:
                closeView = None
                sum = 0
                for view in views:
                    if (closeView is None) or (view.ip == click.ip and click.time >= view.time > closeView.time):
                        closeView = view
                sum += (click.time - closeView.time).seconds
            avg = 0
            if len(clicks) != 0:
                avg = sum / len(clicks)
            avg_click_view_diff_list[ad] = avg
        return avg_click_view_diff_list

    def get_views_per_hour(self, ad):
        views_per_hour = View.objects.annotate(
            hour=TruncHour('time', output_field=DateTimeField()), ).values('hour').filter(ad=ad).annotate(
            views=Count('id'))
        return views_per_hour

    def get_clicks_per_hour(self, ad):
        clicks_per_hour = Click.objects.annotate(
            hour=TruncHour('time', output_field=DateTimeField()), ).values('hour').filter(ad=ad).annotate(
            clicks=Count('id'))
        return clicks_per_hour


class ViewReportPageAPIView(viewsets.ModelViewSet):
    serializer_class = ViewSerializer
    queryset = View.objects.annotate(hour=TruncHour('time', output_field=DateTimeField()), ).values('hour').annotate(
        views=Count('id'))
