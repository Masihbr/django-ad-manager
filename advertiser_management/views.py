from django.shortcuts import render
from .models import Advertiser

# Create your views here.
def home(request):


    context = {
        'advertisers' : Advertiser.objects.all()
    }
    return render(request, 'advertiser_management/ads.html', context)
