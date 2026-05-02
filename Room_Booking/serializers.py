# # the reason we need these serializers is to convert Django model data
# # into another format like JSON that can be processed by the frontend.
# # This way, the API throws JSON to the frontend.

# from rest_framework import serializers
# from .models import Room, RoomImage,OccupiedDate,User

# # It is used to tell which image is bound to which room


# class RoomImageSerializer(serializers.ModelSerializer):
#     room = serializers.HyperlinkedRelatedField(
#         view_name='room-detail',
#         queryset=Room.objects.all()
#     ),
#     class Meta:
#         model = RoomImage
#         fields = ['id', 'image', 'caption', 'room',]


# class RoomSerializer(serializers.HyperlinkedModelSerializer):
#     images = RoomImageSerializer(many=True, read_only=True)
#     class Meta:
#         model = Room
#         fields = [
#             'url',
#             'id',
#             'name',
#             'type',
#             'pricePerNight',
#             'currency',
#             'maxOccupancy',
#             'description',
#             'images'
#         ]


# class OccupiedDateSerializer(serializers.HyperlinkedModelSerializer):
#     room = serializers.HyperlinkedRelatedField(
#         view_name='room-detail',
#         queryset=Room.objects.all()
#     )
#     class Meta:
#         model = OccupiedDate
#         fields = ['url', 'id', 'room', 'date']

# # it is used to hash the password we are creating
# from django.contrib.auth.hashers import make_password

# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model=User
#         fields=['url','id','username','password','email','full_name']

#     def validate_password(self,value):
#         return make_password(value)
from rest_framework import serializers
from .models import Room, RoomImage, OccupiedDate, User
from django.contrib.auth.hashers import make_password

class RoomImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomImage
        fields = ['id', 'image', 'caption']

# class OccupiedDateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OccupiedDate
#         fields = ['id', 'date', 'user']

from rest_framework import serializers
from .models import OccupiedDate

class OccupiedDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OccupiedDate
        fields = ['id', 'room', 'date']   # only include room + date


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

        # Only filter if the user is authenticated
        if request and request.user.is_authenticated:
            if not request.user.is_staff and not request.user.is_superuser:
                qs = qs.filter(user=request.user)
        else:
            # Anonymous users should just see all occupied dates
            qs = qs.none()  # or obj.occupiedDates.all() if you want them visible

        return OccupiedDateSerializer(qs, many=True).data

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'password', 'email', 'full_name']

    def validate_password(self, value):
        return make_password(value)
