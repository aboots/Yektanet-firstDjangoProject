from rest_framework import serializers

from advertiser_management.models import Click, View, Ad, Advertiser


class ClickSerializer(serializers.ModelSerializer):

    class Meta:
        model = Click
        fields = '__all__'


class ViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = View
        fields = '__all__'


class AdSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ad
        fields = '__all__'


class AdvertiserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Advertiser
        fields = '__all__'
