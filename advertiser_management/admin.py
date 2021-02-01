from django.contrib import admin
from .models import Ad,Advertiser,Click,View
# Register your models here.

class AdAdmin(admin.ModelAdmin):
    list_display = ('title','advertiser','url','approve')
    search_fields = ('title',)
    filter_horizontal = ('approve',)

admin.site.register(Ad, AdAdmin)
admin.site.register(Advertiser)
admin.site.register(Click)
admin.site.register(View)
