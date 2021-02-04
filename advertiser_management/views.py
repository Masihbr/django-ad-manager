from collections import OrderedDict

from django.db.models.functions import Trunc, TruncHour, ExtractHour
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.db.models import Count, DateTimeField
from rest_framework import status, generics, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import create_ad_form
from .models import Advertiser, Ad, Click, View
from django.shortcuts import get_object_or_404
from django.views.generic.base import RedirectView, TemplateView

from .serializers import AdSerializer

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated


class GenericAdListAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin,
                           mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin):
    serializer_class = AdSerializer
    queryset = Ad.objects.all()

    lookup_field = 'id'

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)

    def post(self, request, id=None):
        return self.create(request)

    def put(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id=None):
        return self.destroy(request, id)


class AdListAPIView(APIView):
    def get(self, request):
        ads = Ad.objects.all()
        serializer = AdSerializer(ads, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AdSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdEachAPIView(APIView):

    def get_ad(self, pk):
        return get_object_or_404(Ad, pk=pk)

    def get(self, request, pk):
        ad = self.get_ad(pk)
        serializer = AdSerializer(ad)
        return Response(serializer.data)

    def put(self, request, pk):
        ad = self.get_ad(pk)
        serializer = AdSerializer(ad, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        ad = self.get_ad(pk)
        ad.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def ad_list(request):
    if request.method == 'GET':
        ads = Ad.objects.all()
        serializer = AdSerializer(ads, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = AdSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'Delete'])
def ad(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    if request.method == 'GET':
        serializer = AdSerializer(ad)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = AdSerializer(ad, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        ad.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
