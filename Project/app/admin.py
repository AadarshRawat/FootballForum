from django.contrib import admin
from .models import Room,Topic,Message,User

# Register your models here.
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display=['host','topic','name','description','updated','created']

@admin.register(Topic)
class RoomAdmin(admin.ModelAdmin):
    list_display=['name']

@admin.register(Message)
class RoomAdmin(admin.ModelAdmin):
    list_display=['user','room','body','updated','created']

admin.site.register(User)