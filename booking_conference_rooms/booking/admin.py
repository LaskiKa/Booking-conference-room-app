from django.contrib import admin, auth
from .models import Room, RoomBooking
from django.db import models


class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_name', 'seats_number', 'projector')
    list_filter = ('room_name',)


class RoomBookingAdmin(admin.ModelAdmin):
    list_display = ('room_name', 'booking_date', 'comments')

    def room_name(self, Room):
        return Room.room_id.room_name


admin.site.site_header = 'Booking conference room administration'
admin.site.register(Room, RoomAdmin)
admin.site.register(RoomBooking, RoomBookingAdmin)
admin.site.unregister(auth.models.Group)
