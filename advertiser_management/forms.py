from django import forms

class AdForm(forms.Form):
    advertiser_id = forms.IntegerField(label='advertiser_id')
    image = forms.ImageField(label='image')
    title = forms.CharField(label='advertiser_id', max_length=100)
    url = forms.URLField(label='url')