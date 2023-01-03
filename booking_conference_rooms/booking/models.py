from django.db import models

# Create your models here.
class Room(models.Model):
    room_name = models.CharField(max_length=255)
    seats_number = models.SmallIntegerField()
    projector = models.BooleanField(default=False)

class RoomBooking(models.Model):
    booking_date = models.DateField()
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    comments = models.CharField(max_length=255)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['booking_date', 'room_id'], name='uniques_booking')]






