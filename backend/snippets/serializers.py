from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, \
    STYLE_CHOICES, Ping, Manager, Driver, Trip, \
    TripHistory, TripDrowsiness, TripHandsOff
from django.contrib.auth.models import User
from django import forms


class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ['id', 'title', 'code', 'linenos', 'language', 'style']
        owner = serializers.ReadOnlyField(source='owner.username')


class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'snippets']


class PingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ping
        fields = ['id', 'ping']


class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = ['id', 'name', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['id', 'name', 'username', 'password', 'manager', 'trips_count']
        widgets = {
            'password': forms.PasswordInput(),
        }


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ['id', 'start', 'end', 'real_start', 'real_end', 'driver', 'device_id']


class TripHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TripHistory
        fields = ['id', 'trip', 'latitude', 'longitude', 'speed', 'acc_x', 'acc_y', 'acc_z', 'date', 'drowsy_state', 'hands_state']


class TripDrowsinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripDrowsiness
        fields = ['id', 'trip', 'happened_at', 'duration', 'drowsy_ratio']


class TripHandsOffSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripHandsOff
        fields = ['id', 'trip', 'happened_at', 'duration', 'hands_off']

