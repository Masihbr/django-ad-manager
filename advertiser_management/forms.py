from django import forms
from advertiser_management.models import Ad


# class AdForm(forms.Form):
#     advertiser_id = forms.IntegerField(label='Advertiser_id')
#     image = forms.ImageField(label='Image', required=False)
#     title = forms.CharField(label='Title', max_length=100)
#     url = forms.URLField(label='Url')


class create_ad_form(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ('advertiser','title','image','url')
        widgets = {
            'advertiser': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'url':  forms.URLInput(attrs={'class': 'form-control'}),
        }