from django.shortcuts import render, redirect
from django.views.generic import CreateView

from .forms import create_ad_form
from .models import Advertiser, Ad, Click, View
from django.shortcuts import get_object_or_404
from django.views.generic.base import RedirectView


# Create your views here.
def home(request):
    for advertiser in Advertiser.objects.all():
        for ad in advertiser.ad_set.all():
            ad.inc_views()
            # Click.objects.create()
    context = {
        'advertisers': Advertiser.objects.all()
    }
    return render(request, 'advertiser_management/ads.html', context)


class Clicker(RedirectView):
    pattern_name = 'ad'

    def get_redirect_url(self, *args, **kwargs):
        ad = get_object_or_404(Ad, pk=kwargs['pk'])
        ad.inc_clicks()
        return super().get_redirect_url(*args, **kwargs)


def ad(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    context = {
        'ad': ad
    }
    return render(request, 'advertiser_management/ad.html', context)

# def create_ad(request):
#     if request.method == 'POST':
#         form = AdForm(request.POST)
#         if form.is_valid():
#             return redirect('ads')
#     else:
#         form = AdForm()
#     return render(request, 'advertiser_management/ad_form.html', {'form': form})

class CreateAd(CreateView):
    model = Ad
    form_class = create_ad_form
    template_name = 'advertiser_management/ad_form.html'