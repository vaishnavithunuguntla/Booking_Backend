

from django.contrib import admin
from .models import User

from .models import Room,OccupiedDate,RoomImage
# Register your models here.
# Register your models here.
# this willmake sure we will see it in admin panel
admin.site.register(Room)
admin.site.register(User)
admin.site.register(OccupiedDate)
admin.site.register(RoomImage)