from advertiser_management.models import Advertiser,Ad,Click, View
from django.urls import resolve

class IPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        url_name = resolve(request.path_info).url_name
        if url_name == 'ads':
            for advertiser in Advertiser.objects.all():
                for ad in advertiser.ad_set.all():
                    ad.inc_views()
                    view = View(ad=ad, ip=self.get_client_ip(request))
                    view.save()

    def get_client_ip(self, request):
        try:
            x_forward = request.META.get('HTTP_X_FORWARD_FOR')
            if x_forward:
                ip = x_forward.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
        except:
            ip = ''
        return ip
