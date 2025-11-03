from django import forms
from django.contrib.auth.models import User
from .models import Room, Customer, Booking


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean(self):
        cleaned = super().clean()
        p = cleaned.get('password')
        p2 = cleaned.get('password2')
        if p and p2 and p != p2:
            raise forms.ValidationError("Passwords do not match")
        return cleaned


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('number', 'room_type', 'price_per_night', 'is_available')


class CheckinForm(forms.Form):
    name = forms.CharField(max_length=200)
    phone = forms.CharField(max_length=20)
    email = forms.EmailField(required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)
    room = forms.ModelChoiceField(
        queryset=Room.objects.filter(is_available=True))


class CheckoutForm(forms.Form):
    booking_id = forms.IntegerField(label='Booking ID')
