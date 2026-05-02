from rest_framework import serializers
from .models import Room, RoomImage, OccupiedDate, User
from django.contrib.auth.hashers import make_password

# RoomImage serializer
class RoomImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomImage
        fields = ['id', 'image', 'caption']

# OccupiedDate serializer
class OccupiedDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OccupiedDate
        fields = ['id', 'room', 'date']

# Room serializer with nested images + occupiedDates
class RoomSerializer(serializers.HyperlinkedModelSerializer):
    images = RoomImageSerializer(many=True, read_only=True)
    occupiedDates = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = [
            'url',
            'id',
            'name',
            'type',
            'pricePerNight',
            'currency',
            'maxOccupancy',
            'description',
            'images',
            'occupiedDates'
        ]

    def get_occupiedDates(self, obj):
        request = self.context.get('request')
        qs = obj.occupiedDates.all()

        if request and request.user.is_authenticated:
            if not request.user.is_staff and not request.user.is_superuser:
                qs = qs.filter(user=request.user)
        else:
            qs = qs.none()

        return OccupiedDateSerializer(qs, many=True).data

# User serializer (fixed)
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'id', 'email', 'full_name', 'password', 'is_staff', 'is_superuser']

    def validate_password(self, value):
        return make_password(value)
