from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Category, MenuItem, Order, OrderItem, 
    TableBooking, Review, ContactMessage, RestaurantInfo
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'created_at']
    list_editable = ['order']
    search_fields = ['name']


class MenuItemImagePreview(admin.ModelAdmin):
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" style="object-fit: cover;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Preview'


@admin.register(MenuItem)
class MenuItemAdmin(MenuItemImagePreview):
    list_display = ['name', 'category', 'price', 'is_available', 'image_preview', 'created_at']
    list_filter = ['category', 'is_available', 'is_vegetarian', 'is_vegan', 'is_gluten_free']
    search_fields = ['name', 'description']
    list_editable = ['price', 'is_available']
    fieldsets = (
        ('Basic Information', {
            'fields': ('category', 'name', 'description', 'price', 'image')
        }),
        ('Dietary Information', {
            'fields': ('is_vegetarian', 'is_vegan', 'is_gluten_free', 'spice_level')
        }),
        ('Availability', {
            'fields': ('is_available', 'preparation_time')
        }),
    )


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['menu_item', 'quantity', 'price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'customer_phone', 'status', 'total_amount', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['customer_name', 'customer_email', 'customer_phone']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [OrderItemInline]
    fieldsets = (
        ('Customer Information', {
            'fields': ('customer_name', 'customer_email', 'customer_phone', 'customer_address')
        }),
        ('Order Details', {
            'fields': ('status', 'total_amount', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ['total_amount']
        return self.readonly_fields


@admin.register(TableBooking)
class TableBookingAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'customer_phone', 'booking_date', 'booking_time', 
                    'number_of_guests', 'status', 'created_at']
    list_filter = ['status', 'booking_date', 'created_at']
    search_fields = ['customer_name', 'customer_email', 'customer_phone']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Customer Information', {
            'fields': ('customer_name', 'customer_email', 'customer_phone')
        }),
        ('Booking Details', {
            'fields': ('booking_date', 'booking_time', 'number_of_guests', 'status', 'special_requests')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    date_hierarchy = 'booking_date'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'rating', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'rating', 'created_at']
    search_fields = ['customer_name', 'review_text']
    list_editable = ['is_approved']
    readonly_fields = ['created_at']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Show pending reviews first
        return qs.order_by('is_approved', '-created_at')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    list_editable = ['is_read']
    readonly_fields = ['created_at']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Show unread messages first
        return qs.order_by('is_read', '-created_at')


@admin.register(RestaurantInfo)
class RestaurantInfoAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'tagline', 'description')
        }),
        ('Contact Details', {
            'fields': ('phone', 'email', 'address', 'whatsapp_number', 'google_maps_link')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'instagram_url', 'twitter_url')
        }),
        ('Business Hours', {
            'fields': ('opening_hours',)
        }),
    )
    
    def has_add_permission(self, request):
        # Prevent adding more than one instance
        return not RestaurantInfo.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion
        return False
