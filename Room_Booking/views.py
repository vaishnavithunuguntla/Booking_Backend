# from django.contrib.auth import authenticate
# from django.shortcuts import render
# from rest_framework import generics, permissions
# from rest_framework.decorators import api_view
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.reverse import reverse
# from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.authtoken.models import Token

# from .models import Room, OccupiedDate, User
# from .permissions import IsAdminOrReadOnly
# from .serializers import RoomSerializer, OccupiedDateSerializer, UserSerializer


# # Entry point where we list all the APIs
# @api_view(['GET'])
# def api_root(request, format=None):
#     return Response({
#         'rooms': reverse('room-list', request=request, format=format),
#         'occupied-dates': reverse('occupieddate-list', request=request, format=format),
#         'users': reverse('user-list', request=request, format=format),
#     })


# # -------------------- ROOMS --------------------
# # -------------------- ROOMS --------------------
# from rest_framework import generics, permissions
# from .models import Room
# from .serializers import RoomSerializer

# class RoomList(generics.ListCreateAPIView):
#     queryset = Room.objects.all()
#     serializer_class = RoomSerializer
#     permission_classes = [permissions.AllowAny]

#     def get_serializer_context(self):
#         return {'request': self.request}

# class RoomDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Room.objects.all()
#     serializer_class = RoomSerializer
#     permission_classes = [permissions.AllowAny]
#     def get_serializer_context(self):
#         return {'request': self.request}



# # -------------------- OCCUPIED DATES --------------------
# # -------------------- OCCUPIED DATES --------------------
# from .models import OccupiedDate
# from .serializers import OccupiedDateSerializer

# class OccupiedDatesList(generics.ListCreateAPIView):
#     queryset = OccupiedDate.objects.all()
#     serializer_class = OccupiedDateSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#     # logged-in users can create bookings, anonymous can only read

# class OccupiedDatesDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = OccupiedDate.objects.all()
#     serializer_class = OccupiedDateSerializer
#     permission_classes = [permissions.IsAuthenticated]




# # -------------------- USERS --------------------
# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

#     def get_queryset(self):
#         user = self.request.user
#         if user.is_staff or user.is_superuser:
#             return User.objects.all()
#         return User.objects.filter(id=user.id)


# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

#     def get_object(self):
#         user = self.request.user
#         obj = super().get_object()
#         if obj == user or user.is_staff or user.is_superuser:
#             return obj
#         raise PermissionDenied("You do not have permission to access this user's details")


# # -------------------- AUTH --------------------
# class Register(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

#     def perform_create(self, serializer):
#         user = serializer.save()
#         token, created = Token.objects.get_or_create(user=user)
#         self.response_data = {
#             "user": {
#                 "id": user.id,
#                 "username": user.username,
#                 "email": user.email,
#                 "full_name": user.full_name
#             },
#             "token": token.key
#         }

#     def create(self, request, *args, **kwargs):
#         super().create(request, *args, **kwargs)
#         return Response(self.response_data)


# class Login(APIView):
#     def post(self, request, *args, **kwargs):
#         username = request.data.get("username")
#         password = request.data.get("password")

#         user = authenticate(username=username, password=password)
#         if user is None:
#             raise AuthenticationFailed('Invalid username or password')

#         token, created = Token.objects.get_or_create(user=user)
#         return Response({
#             "user": {
#                 "id": user.id,
#                 "username": user.username,
#                 "email": user.email,
#                 "full_name": user.full_name
#             },
#             "token": token.key
#         })


# class TestToken(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         return Response({"message": "Token is valid!", "user": request.user.username})




from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from .models import Room, OccupiedDate, User
from .permissions import IsAdminOrReadOnly
from .serializers import RoomSerializer, OccupiedDateSerializer, UserSerializer


# Entry point where we list all the APIs
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'rooms': reverse('room-list', request=request, format=format),
        'occupied-dates': reverse('occupieddate-list', request=request, format=format),
        'users': reverse('user-list', request=request, format=format),
    })


# -------------------- ROOMS --------------------
# -------------------- ROOMS --------------------
from rest_framework import generics, permissions
from .models import Room
from .serializers import RoomSerializer

class RoomList(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.AllowAny]

    def get_serializer_context(self):
        return {'request': self.request}

class RoomDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.AllowAny]
    def get_serializer_context(self):
        return {'request': self.request}



# -------------------- OCCUPIED DATES --------------------
# -------------------- OCCUPIED DATES --------------------
from .models import OccupiedDate
from .serializers import OccupiedDateSerializer

class OccupiedDatesList(generics.ListCreateAPIView):
    queryset = OccupiedDate.objects.all()
    serializer_class = OccupiedDateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Automatically assign the logged-in user
        serializer.save(user=self.request.user)


class OccupiedDatesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = OccupiedDate.objects.all()
    serializer_class = OccupiedDateSerializer
    permission_classes = [permissions.IsAuthenticated]




# -------------------- USERS --------------------
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return User.objects.all()
        return User.objects.filter(id=user.id)


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        user = self.request.user
        obj = super().get_object()
        if obj == user or user.is_staff or user.is_superuser:
            return obj
        raise PermissionDenied("You do not have permission to access this user's details")


# -------------------- AUTH --------------------
class Register(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        self.response_data = {
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name
            },
            "token": token.key
        }

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response(self.response_data)


class Login(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user is None:
            raise AuthenticationFailed('Invalid username or password')

        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name
            },
            "token": token.key
        })


class TestToken(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Token is valid!", "user": request.user.username})

