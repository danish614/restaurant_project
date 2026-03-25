from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
import json

from .models import (
    MenuItem, Category, Order, OrderItem, 
    TableBooking, Review, ContactMessage, RestaurantInfo
)
from .forms import OrderForm, TableBookingForm, ReviewForm, ContactForm


def home(request):
    """Homepage view"""
    categories = Category.objects.all()[:3]  # Featured categories
    featured_items = MenuItem.objects.filter(is_available=True)[:6]
    reviews = Review.objects.filter(is_approved=True)[:3]
    restaurant_info = RestaurantInfo.get_info()
    
    context = {
        'categories': categories,
        'featured_items': featured_items,
        'reviews': reviews,
        'restaurant_info': restaurant_info,
    }
    return render(request, 'core/home.html', context)


def menu(request):
    """Menu page view"""
    categories = Category.objects.prefetch_related('items').all()
    restaurant_info = RestaurantInfo.get_info()
    
    context = {
        'categories': categories,
        'restaurant_info': restaurant_info,
    }
    return render(request, 'core/menu.html', context)


def order_online(request):
    """Online ordering page"""
    categories = Category.objects.prefetch_related('items').filter(items__is_available=True).distinct()
    restaurant_info = RestaurantInfo.get_info()
    
    context = {
        'categories': categories,
        'restaurant_info': restaurant_info,
    }
    return render(request, 'core/order.html', context)


@require_POST
def create_order(request):
    """Handle order creation via AJAX"""
    try:
        data = json.loads(request.body)
        
        # Create order
        order = Order.objects.create(
            customer_name=data['customer_name'],
            customer_email=data['customer_email'],
            customer_phone=data['customer_phone'],
            customer_address=data['customer_address'],
            notes=data.get('notes', ''),
            total_amount=Decimal(data['total_amount'])
        )
        
        # Create order items
        for item in data['items']:
            menu_item = MenuItem.objects.get(id=item['id'])
            OrderItem.objects.create(
                order=order,
                menu_item=menu_item,
                quantity=item['quantity'],
                price=menu_item.price,
                notes=item.get('notes', '')
            )
        
        return JsonResponse({
            'success': True,
            'order_id': order.id,
            'message': 'Order placed successfully! We will contact you shortly.'
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error placing order: {str(e)}'
        }, status=400)


def table_booking(request):
    """Table booking page"""
    restaurant_info = RestaurantInfo.get_info()
    
    if request.method == 'POST':
        form = TableBookingForm(request.POST)
        if form.is_valid():
            booking = form.save()
            messages.success(request, 
                f'Table booking request submitted successfully! We will confirm your reservation for '
                f'{booking.booking_date} at {booking.booking_time} shortly.')
            return redirect('table_booking')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TableBookingForm()
    
    context = {
        'form': form,
        'restaurant_info': restaurant_info,
    }
    return render(request, 'core/booking.html', context)


def reviews(request):
    """Reviews page"""
    approved_reviews = Review.objects.filter(is_approved=True)
    restaurant_info = RestaurantInfo.get_info()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your review! It will be published after approval.')
            return redirect('reviews')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ReviewForm()
    
    context = {
        'reviews': approved_reviews,
        'form': form,
        'restaurant_info': restaurant_info,
    }
    return render(request, 'core/reviews.html', context)


def contact(request):
    """Contact page"""
    restaurant_info = RestaurantInfo.get_info()
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully! We will get back to you soon.')
            return redirect('contact')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
        'restaurant_info': restaurant_info,
    }
    return render(request, 'core/contact.html', context)


@require_POST
def get_menu_item(request, item_id):
    """Get menu item details via AJAX"""
    try:
        item = MenuItem.objects.get(id=item_id, is_available=True)
        data = {
            'id': item.id,
            'name': item.name,
            'description': item.description,
            'price': float(item.price),
            'image': item.image.url if item.image else '',
            'is_vegetarian': item.is_vegetarian,
            'is_vegan': item.is_vegan,
            'is_gluten_free': item.is_gluten_free,
            'spice_level': item.spice_level,
        }
        return JsonResponse(data)
    except MenuItem.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)
