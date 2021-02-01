from django.shortcuts import render, redirect
from django.views.generic import CreateView

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
    template_name = "report.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ads_list'] = Ad.objects.all()[:5]
        return context
