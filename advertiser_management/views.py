from django.shortcuts import render
from .models import Advertiser


# Create your views here.
def home(request):
    for advertiser in Advertiser.objects.all():
        for ad in advertiser.ad_set.all():
            ad.inc_views()
    context = {
        'advertisers': Advertiser.objects.all()
    }
    return render(request, 'advertiser_management/ads.html', context)