# from django.db import models
# from django.contrib.auth.models import AbstractUser

# class Room(models.Model):
#     ROOM_TYPES = [
#         ('suite', 'Suite'),
#         ('standard', 'Standard Room'),
#         ('deluxe', 'Deluxe Room'),
#     ]
#     CURRENCY_TYPES = [
#         ('USD', 'USD'),
#         ('INR', 'INR'),
#         ('EUR', 'EUR'),
#     ]
#     name = models.CharField(max_length=100, blank=True, default='')
#     type = models.CharField(max_length=100, choices=ROOM_TYPES)
#     pricePerNight = models.IntegerField(default=150)
#     currency = models.CharField(default="USD", max_length=10, choices=CURRENCY_TYPES)
#     maxOccupancy = models.IntegerField(default=1)
#     description = models.TextField(max_length=1000)

#     def __str__(self):
#         return f"{self.name} ({self.type})"


# class RoomImage(models.Model):
#     image = models.ImageField(upload_to='room_images/')
#     caption = models.CharField(max_length=255, blank=True, null=True)
#     room = models.ForeignKey(Room, related_name='images', on_delete=models.CASCADE)

#     def __str__(self):
#         return f"Image for {self.room.name} - {self.caption or 'No Caption'}"


# class OccupiedDate(models.Model):
#     room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="occupiedDates")
#     user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="booked_dates")
#     date = models.DateField()

#     def __str__(self):
#         return f"{self.date} - {self.room.name} booked by {self.user.username}"


# class User(AbstractUser):
#     email = models.EmailField(unique=True)
#     full_name = models.CharField(max_length=100, default="")

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, full_name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100, default="")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"          # login with email
    REQUIRED_FIELDS = ["full_name"]   # asked when creating superuser

    objects = UserManager()

    def __str__(self):
        return self.email


class Room(models.Model):
    ROOM_TYPES = [
        ('suite', 'Suite'),
        ('standard', 'Standard Room'),
        ('deluxe', 'Deluxe Room'),
    ]
    CURRENCY_TYPES = [
        ('USD', 'USD'),
        ('INR', 'INR'),
        ('EUR', 'EUR'),
    ]
    name = models.CharField(max_length=100, blank=True, default='')
    type = models.CharField(max_length=100, choices=ROOM_TYPES)
    pricePerNight = models.IntegerField(default=150)
    currency = models.CharField(default="USD", max_length=10, choices=CURRENCY_TYPES)
    maxOccupancy = models.IntegerField(default=1)
    description = models.TextField(max_length=1000)

    def __str__(self):
        return f"{self.name} ({self.type})"


class RoomImage(models.Model):
    image = models.ImageField(upload_to='room_images/')
    caption = models.CharField(max_length=255, blank=True, null=True)
    room = models.ForeignKey(Room, related_name='images', on_delete=models.CASCADE)

    def __str__(self):
        return f"Image for {self.room.name} - {self.caption or 'No Caption'}"


class OccupiedDate(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="occupiedDates")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="booked_dates")
    date = models.DateField()

    def __str__(self):
        return f"{self.date} - {self.room.name} booked by {self.user.email}"
