from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Booking, Room
from django.utils import timezone


@receiver(post_save, sender=Booking)
def update_room_availability_on_booking(sender, instance, created, **kwargs):
    # on create (check-in), mark room unavailable
    if created:
        room = instance.room
        room.is_available = False
        room.save()


@receiver(post_save, sender=Booking)
def update_room_availability_on_checkout(sender, instance, **kwargs):
    # when booking updated to checked out, mark room available
    if instance.is_checked_out and instance.checkout_datetime:
        room = instance.room
        room.is_available = True
        room.save()
