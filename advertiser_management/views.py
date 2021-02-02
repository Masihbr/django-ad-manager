from collections import OrderedDict

from django.db.models.functions import Trunc, TruncHour, ExtractHour
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.db.models import Count, DateTimeField
from .forms import create_ad_form
from .models import Advertiser, Ad, Click, View
from django.shortcuts import get_object_or_404
from django.views.generic.base import RedirectView, TemplateView


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
        ad.inc_clicks()
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

        context = {
            'clicks_per_views_list': clicks_per_views_list,
            'clicks_views_sum_list': clicks_views_sum_list,
            'ads_list': Ad.objects.all()
        }
        return context

    def get_clicks_per_view_list(self):
        clicks_per_views_list = {}
        for ad in Ad.objects.all():
            list = {}
            clicks_per_hour = Click.objects.annotate(
                hour=TruncHour('time', output_field=DateTimeField()), ).values('hour').filter(ad=ad).annotate(
                clicks=Count('id'))
            views_per_hour = View.objects.annotate(
                hour=TruncHour('time', output_field=DateTimeField()), ).values('hour').filter(ad=ad).annotate(
                views=Count('id'))
            for v in views_per_hour:
                list[v['hour']] = v['views']
            for c in clicks_per_hour:
                if list.keys().__contains__(c['hour']):
                    list[c['hour']] = c['clicks'] / list[c['hour']]
                else:
                    list[c['hour']] = 0
            clicks_per_views_list[ad] = sorted(list.items(),reverse=True, key=lambda t: t[1])
        return clicks_per_views_list

    def get_clicks_views_sum_list(self):
        clicks_views_sum_list = {}
        for ad in Ad.objects.all():
            list = {}
            clicks_per_hour = Click.objects.annotate(
                hour=TruncHour('time', output_field=DateTimeField()), ).values('hour').filter(ad=ad).annotate(
                clicks=Count('id'))
            views_per_hour = View.objects.annotate(
                hour=TruncHour('time', output_field=DateTimeField()), ).values('hour').filter(ad=ad).annotate(
                views=Count('id'))
            for c in clicks_per_hour:
                list[c['hour']] = c['clicks']
            for v in views_per_hour:
                if list.keys().__contains__(v['hour']):
                    list[v['hour']] += v['views']
                else:
                    list[v['hour']] = v['views']
            clicks_views_sum_list[ad] = sorted(list.items(), key=lambda t: t[0])
        return clicks_views_sum_list
