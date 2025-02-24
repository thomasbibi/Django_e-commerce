from django.contrib import admin
from .models import Profile, Product, Cart, CartItem, Order, OrderItem, Payment

# Custom Admin for Profile
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'created_at')
    search_fields = ('user__username', 'user__email')
    list_filter = ('created_at',)

admin.site.register(Profile, ProfileAdmin)

# Custom Admin for Product
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at',)

admin.site.register(Product, ProductAdmin)

# Custom Admin for Cart
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]
    list_display = ('user', 'created_at')
    search_fields = ('user__username', 'user__email')
    list_filter = ('created_at',)

admin.site.register(Cart, CartAdmin)

# Custom Admin for Order
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ('id', 'user', 'total_price', 'status', 'created_at')
    search_fields = ('user__username', 'user__email')
    list_filter = ('status', 'created_at')
    actions = ['mark_as_shipped', 'mark_as_delivered']

    def mark_as_shipped(self, request, queryset):
        queryset.update(status='shipped')
    mark_as_shipped.short_description = "Mark selected orders as shipped"

    def mark_as_delivered(self, request, queryset):
        queryset.update(status='delivered')
    mark_as_delivered.short_description = "Mark selected orders as delivered"

admin.site.register(Order, OrderAdmin)

# Custom Admin for Payment
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'stripe_charge_id', 'amount', 'timestamp')
    search_fields = ('order__user__username', 'stripe_charge_id')
    list_filter = ('timestamp',)

admin.site.register(Payment, PaymentAdmin)