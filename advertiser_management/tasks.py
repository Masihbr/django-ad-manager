from datetime import timezone, timedelta

from celery import shared_task
from .models import Ad, Click, View, HourStatusTable
import time


@shared_task
def save_hour_ad_status():
    ads = Ad.objects.all()
    this_hour = timezone.now().replace(minute=0, second=0, microsecond=0)
    past_hour = this_hour - timedelta(hours=1)
    for ad in ads:
        clicks = Click.objects.filter(ad=ad, date__range=(past_hour, this_hour)).count()
        views = View.objects.filter(ad=ad, date__range=(past_hour, this_hour)).count()
        table = HourStatusTable(ad=ad, clicks=clicks, views=views, date=this_hour)
        table.save()


# @shared_task

