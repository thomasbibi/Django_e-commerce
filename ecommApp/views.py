from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import Q
from .models import Product, Cart, CartItem, Order, OrderItem, Payment
import stripe
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

# Stripe API key
stripe.api_key = settings.STRIPE_SECRET_KEY

# Homepage View
def index(request):
    products = Product.objects.all()
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    return render(request, 'index.html', {'products': products})

# Product Detail View
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart, product=product
        )
        if not item_created:
            cart_item.quantity += quantity
            cart_item.save()
        else:
            cart_item.quantity = quantity
            cart_item.save()
        messages.success(request, f"{product.title} added to cart!")
        return redirect('cart')
    return render(request, 'product_detail.html', {'product': product})

# Cart View
@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    for item in cart_items:
        item.total = item.product.price * item.quantity

    if request.method == 'POST':
        action = request.POST.get('action')
        item_id = request.POST.get('item_id')

        if action == 'update':
            quantity = int(request.POST.get('quantity', 1))
            cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
            if quantity > 0:
                cart_item.quantity = quantity
                cart_item.save()
                messages.success(request, "Cart updated!")
            else:
                cart_item.delete()
                messages.success(request, "Item removed from cart!")

        elif action == 'remove':
            cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
            cart_item.delete()
            messages.success(request, "Item removed from cart!")

        elif action == 'clear':
            cart.items.all().delete()
            messages.success(request, "Cart cleared!")

        return redirect('cart')

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })

# Checkout View
@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.all()
    if not cart_items:
        messages.error(request, "Your cart is empty!")
        return redirect('cart')

    total_price = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        # Create Order
        order = Order.objects.create(
            user=request.user,
            total_price=total_price,
            status='pending'
        )
        
        # Move cart items to order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        # Stripe Payment Processing
        try:
            charge = stripe.Charge.create(
                amount=int(total_price * 100),  
                currency='usd',
                description=f'Order {order.id}',
                source=request.POST['stripeToken'],
            )
            Payment.objects.create(
                order=order,
                stripe_charge_id=charge['id'],
                amount=total_price
            )
            # Clear cart
            cart.items.all().delete()
            messages.success(request, "Payment successful! Order placed.")
            return redirect('order_confirmation', order_id=order.id)
        except stripe.error.StripeError as e:
            messages.error(request, f"Payment error: {str(e)}")
            return redirect('checkout')

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
    })

# Order Confirmation View
@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_confirmation.html', {'order': order})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('index')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})