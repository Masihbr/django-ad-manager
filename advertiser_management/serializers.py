from rest_framework import serializers

from advertiser_management.models import Ad, Advertiser, Click, View


class AdSerializer(serializers.Serializer):
    class Meta:
        model = Ad
        fields = '__all__'

    def create(self, validated_data):
        return Ad.objects.create(**validated_data)


class AdvertiserSerializer(serializers.Serializer):
    class Meta:
        model = Advertiser
        fields = '__all__'

    def create(self, validated_data):
        return Advertiser.objects.create(**validated_data)


class ClickSerializer(serializers.Serializer):
    class Meta:
        model = Click
        fields = '__all__'


class AdSerializer(serializers.Serializer):
    class Meta:
        model = View
        fields = '__all__'
