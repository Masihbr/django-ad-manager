from rest_framework import serializers

from advertiser_management.models import Ad, Advertiser, Click, View


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'

    def create(self, validated_data):
        return Ad.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.image = validated_data.get('image', instance.image)
        instance.advertiser = validated_data.get('advertiser', instance.advertiser)
        instance.url = validated_data.get('url', instance.url)
        instance.approve = validated_data.get('approve', instance.approve)
        instance.save()
        return instance


class AdvertiserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertiser
        fields = '__all__'

    def create(self, validated_data):
        return Advertiser.objects.create(**validated_data)


class ClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = Click
        fields = '__all__'


class ViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = View
        fields = '__all__'
