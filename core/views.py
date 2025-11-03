from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db import transaction
from math import ceil

from .forms import RegisterForm, LoginForm, RoomForm, CheckinForm, CheckoutForm
from .models import Room, Customer, Booking

# ----- auth -----


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Account created. Please login.")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(request, username=u, password=p)
            if user:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid credentials")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')

# ----- dashboard -----


@login_required
def dashboard(request):
    # show key stats
    total_rooms = Room.objects.count()
    available_rooms = Room.objects.filter(is_available=True).count()
    active_bookings_qs = Booking.objects.filter(is_checked_out=False).select_related(
        'customer', 'room').order_by('checkin_datetime')

    # number of active bookings
    active_bookings = active_bookings_qs.count()

    # Prepare a small list to pass to template (optional: you can pass queryset directly)
    active_list = []
    for b in active_bookings_qs:
        active_list.append({
            'booking_id': b.id,
            'customer_name': b.customer.name,
            'customer_phone': b.customer.phone,
            'room_number': b.room.number,
            'room_type': b.room.get_room_type_display(),
            'checkin': b.checkin_datetime,
        })

    context = {
        'total_rooms': total_rooms,
        'available_rooms': available_rooms,
        'active_bookings': active_bookings,
        'active_list': active_list,         # pass the list to template
    }
    return render(request, 'dashboard.html', context)

# ----- rooms -----


@login_required
def room_list(request):
    rooms = Room.objects.all().order_by('number')
    return render(request, 'rooms/list.html', {'rooms': rooms})


@login_required
def room_add(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Room added")
            return redirect('room_list')
    else:
        form = RoomForm()
    return render(request, 'rooms/add.html', {'form': form})


@login_required
def room_delete(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        room.delete()
        messages.success(request, "Room deleted")
        return redirect('room_list')
    return render(request, 'rooms/delete_confirm.html', {'room': room})

# ----- checkin -----


@login_required
@transaction.atomic
def checkin_view(request):
    if request.method == 'POST':
        form = CheckinForm(request.POST)
        if form.is_valid():
            # create customer
            customer = Customer.objects.create(
                name=form.cleaned_data['name'],
                phone=form.cleaned_data['phone'],
                email=form.cleaned_data.get('email') or '',
                address=form.cleaned_data.get('address') or ''
            )
            room = form.cleaned_data['room']
            # create booking - checkin time = now
            booking = Booking.objects.create(
                customer=customer, room=room, checkin_datetime=timezone.now())
            # signals (if present) will mark room unavailable
            messages.success(
                request, f'Check-in successful. Booking ID: {booking.id}')
            return redirect('bill', booking_id=booking.id)
    else:
        form = CheckinForm()
    return render(request, 'checkin.html', {'form': form})

# ----- checkout -----


@login_required
@transaction.atomic
def checkout_view(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            bid = form.cleaned_data['booking_id']
            try:
                booking = Booking.objects.get(id=bid)
            except Booking.DoesNotExist:
                messages.error(request, "Booking ID not found")
                return redirect('checkout')

            if booking.is_checked_out:
                messages.info(request, "This booking is already checked out")
                return redirect('bill', booking_id=booking.id)

            # process checkout
            booking.checkout_datetime = timezone.now()
            # calculate nights: at least 1 night
            delta = booking.checkout_datetime - booking.checkin_datetime
            nights = ceil(delta.total_seconds() / (24 * 3600))
            if nights < 1:
                nights = 1
            amount = nights * float(booking.room.price_per_night)
            booking.total_amount = amount
            booking.is_checked_out = True
            booking.save()
            # signals (if wired) will mark room available
            messages.success(request, f'Checkout successful. Total: {amount}')
            return redirect('bill', booking_id=booking.id)
    else:
        form = CheckoutForm()
    return render(request, 'checkout.html', {'form': form})


@login_required
def bill_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    # compute displayable nights if checkout done, else compute till now
    if booking.checkout_datetime:
        delta = booking.checkout_datetime - booking.checkin_datetime
    else:
        delta = timezone.now() - booking.checkin_datetime
    nights = ceil(delta.total_seconds() / (24 * 3600))
    if nights < 1:
        nights = 1
    computed_amount = nights * float(booking.room.price_per_night)
    context = {
        'booking': booking,
        'nights': nights,
        'computed_amount': computed_amount,
    }
    return render(request, 'bill.html', context)
