from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.utils import timezone


class Room(models.Model):
    ROOM_TYPES = [
        ('single', 'Single'),
        ('double', 'Double'),
        ('suite', 'Suite'),
    ]

    number = models.CharField(
        max_length=10, unique=True)   # room number / code
    room_type = models.CharField(
        max_length=10, choices=ROOM_TYPES, default='single')
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Room {self.number} ({self.room_type})'


class Customer(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.phone}'


class Booking(models.Model):
    # We'll use the default AutoField 'id' as the auto-incrementing booking id.
    # This is the "customer id" you can give during checkout (booking.id).
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(
        Room, on_delete=models.PROTECT, related_name='bookings')
    checkin_datetime = models.DateTimeField(default=timezone.now)
    checkout_datetime = models.DateTimeField(blank=True, null=True)
    is_checked_out = models.BooleanField(default=False)
    # store computed bill when checkout happens
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Booking {self.id} — {self.customer.name} — Room {self.room.number}'
