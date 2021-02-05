from datetime import timedelta

from celery import shared_task
from django.db.models import Sum
from django.utils import timezone

from .models import Ad, Click, View, HourStatusTable, DayStatusTable
import time


@shared_task
def save_hourly_ad_status():
    ads = Ad.objects.all()
    this_hour = timezone.now().replace(minute=0, second=0, microsecond=0)
    past_hour = this_hour - timedelta(hours=1)
    for ad in ads:
        clicks = Click.objects.filter(ad=ad, time__range=(past_hour, this_hour)).count()
        views = View.objects.filter(ad=ad, time__range=(past_hour, this_hour)).count()
        table = HourStatusTable(ad=ad, clicks=clicks, views=views, date=this_hour)
        table.save()


@shared_task
def save_daily_ad_status():
    ads = Ad.objects.all()
    this_day = timezone.now().replace(minute=0, second=0, microsecond=0)
    past_day = this_day - timedelta(days=1)
    for ad in ads:
        hour_status_table = HourStatusTable.objects.filter(ad=ad, date__range=(past_day, this_day)).aggregate(
            clicks_sum=Sum('clicks'), views_sum=Sum('views'))
        clicks = hour_status_table['clicks_sum']
        views = hour_status_table['views_sum']
        table = DayStatusTable(ad=ad, clicks=clicks, views=views, date=this_day)
        table.save()