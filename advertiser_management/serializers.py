from rest_framework import serializers

from advertiser_management.models import Ad, Advertiser, Click, View


class AdSerializer(serializers.Serializer):
    class Meta:
        model = Ad
        fields = '__all__'


class AdvertiserSerializer(serializers.Serializer):
    class Meta:
        model = Advertiser
        fields = '__all__'


class ClickSerializer(serializers.Serializer):
    class Meta:
        model = Click
        fields = '__all__'


class AdSerializer(serializers.Serializer):
    class Meta:
        model = View
        fields = '__all__'
