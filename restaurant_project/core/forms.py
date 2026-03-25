from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Order, OrderItem, TableBooking, Review, ContactMessage


class OrderForm(forms.ModelForm):
    """Form for online orders"""
    class Meta:
        model = Order
        fields = ['customer_name', 'customer_email', 'customer_phone', 'customer_address', 'notes']
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full Name',
                'required': True
            }),
            'customer_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address',
                'required': True
            }),
            'customer_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number',
                'required': True
            }),
            'customer_address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Delivery Address',
                'rows': 3,
                'required': True
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Special instructions (optional)',
                'rows': 2
            }),
        }


class TableBookingForm(forms.ModelForm):
    """Form for table reservations"""
    class Meta:
        model = TableBooking
        fields = ['customer_name', 'customer_email', 'customer_phone', 
                 'number_of_guests', 'booking_date', 'booking_time', 'special_requests']
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full Name',
                'required': True
            }),
            'customer_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address',
                'required': True
            }),
            'customer_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number',
                'required': True
            }),
            'number_of_guests': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Number of Guests',
                'min': '1',
                'max': '20',
                'required': True
            }),
            'booking_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'booking_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
                'required': True
            }),
            'special_requests': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Any special requests? (optional)',
                'rows': 3
            }),
        }
    
    def clean_booking_date(self):
        booking_date = self.cleaned_data.get('booking_date')
        if booking_date < timezone.now().date():
            raise ValidationError("Booking date cannot be in the past.")
        # Max 60 days in advance
        if booking_date > (timezone.now().date() + timedelta(days=60)):
            raise ValidationError("Bookings can only be made up to 60 days in advance.")
        return booking_date
    
    def clean(self):
        cleaned_data = super().clean()
        booking_date = cleaned_data.get('booking_date')
        booking_time = cleaned_data.get('booking_time')
        
        if booking_date and booking_time:
            # Check if booking is at least 2 hours from now
            booking_datetime = datetime.combine(booking_date, booking_time)
            now = timezone.now()
            
            # Make booking_datetime timezone-aware
            if timezone.is_naive(booking_datetime):
                booking_datetime = timezone.make_aware(booking_datetime)
            
            if booking_datetime < (now + timedelta(hours=2)):
                raise ValidationError("Bookings must be made at least 2 hours in advance.")
            
            # Check if time slot is already booked (exclude current instance if editing)
            existing_booking = TableBooking.objects.filter(
                booking_date=booking_date,
                booking_time=booking_time,
                status__in=['pending', 'confirmed']
            )
            
            if self.instance.pk:
                existing_booking = existing_booking.exclude(pk=self.instance.pk)
            
            if existing_booking.exists():
                raise ValidationError("This time slot is already booked. Please choose a different time.")
        
        return cleaned_data


class ReviewForm(forms.ModelForm):
    """Form for customer reviews"""
    class Meta:
        model = Review
        fields = ['customer_name', 'customer_email', 'rating', 'review_text']
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name',
                'required': True
            }),
            'customer_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address',
                'required': True
            }),
            'rating': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }, choices=[(i, f'{i} Star{"s" if i != 1 else ""}') for i in range(1, 6)]),
            'review_text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Share your experience...',
                'rows': 4,
                'required': True
            }),
        }


class ContactForm(forms.ModelForm):
    """Form for contact messages"""
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number (optional)'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subject',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Your Message',
                'rows': 5,
                'required': True
            }),
        }
