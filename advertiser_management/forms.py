from django import forms

class AdForm(forms.Form):
    advertiser_id = forms.IntegerField(label='Advertiser_id')
    image = forms.ImageField(label='Image')
    title = forms.CharField(label='Title', max_length=100)
    url = forms.URLField(label='Url')