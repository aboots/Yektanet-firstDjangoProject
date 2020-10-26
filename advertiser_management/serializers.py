from rest_framework import serializers

from advertiser_management.models import Click, View, Ad, Advertiser


class ClickSerializer(serializers.models):

    class Meta:
        model = Click
        fields = '__all__'


class ViewSerializer(serializers.models):

    class Meta:
        model = View
        fields = '__all__'


class AdSerializer(serializers.models):

    class Meta:
        model = Ad
        fields = '__all__'


class AdvertiserSerializer(serializers.models):

    class Meta:
        model = Advertiser
        fields = '__all__'
