from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Product, Category, Cart, Order, Review,Address
from .forms import SignupForm, LoginForm, ReviewForm
from django.contrib.auth import get_user_model
from django.contrib import messages


# Fetch CustomUser model
CustomUser = get_user_model()

def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    # Search functionality
    query = request.GET.get('q', '')
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query) | Q(category__name__icontains=query)
        )

    return render(request, 'ecommerce_app/home.html', {
        'categories': categories,
        'products': products,
        'query': query
    })

@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.all()
    review_form = ReviewForm()

    if request.method == "POST":
        if 'quantity' in request.POST:
            quantity = int(request.POST.get('quantity', 1))
            cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
            cart_item.quantity += quantity
            cart_item.save()
            #return redirect('cart')

        elif 'content' in request.POST and 'rating' in request.POST:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.user = request.user
                review.product = product
                review.save()
                return redirect('product_detail', product_id=product.id)

    return render(request, 'ecommerce_app/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'review_form': review_form,
    })

@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    
    # Calculate total for each item and overall total
    cart_item_totals = [
        {
            'product': item.product,
            'quantity': item.quantity,
            'total': item.product.price * item.quantity
        }
        for item in cart_items
    ]
    
    total = sum(item['total'] for item in cart_item_totals)
    
    return render(request, 'ecommerce_app/cart.html', {
        'cart_items': cart_item_totals,
        'total': total,
    })

@login_required
def update_quantity(request, product_id):
    """Update the quantity of an item in the cart."""
    if request.method == 'POST':
        cart_item = get_object_or_404(Cart, user=request.user, product_id=product_id)
        quantity = int(request.POST.get('quantity', 1))

        # Ensure quantity is valid
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
        
        return redirect('cart')

@login_required
def remove_item(request, product_id):
    """Remove an item from the cart."""
    cart_item = get_object_or_404(Cart, user=request.user, product_id=product_id)
    cart_item.delete()
    return redirect('cart')


@login_required
def checkout(request):
    # Fetch cart items for the logged-in user
    cart_items = Cart.objects.filter(user=request.user)

    # Calculate the total price for each cart item and the overall total price
    total_price = 0
    cart_item_details = []

    for item in cart_items:
        item_total = item.product.price * item.quantity
        total_price += item_total
        cart_item_details.append({
            'product': item.product,
            'quantity': item.quantity,
            'item_total': item_total
        })

    if request.method == 'POST':
        # Extract form data
        street_address = request.POST.get('address')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')
        country = request.POST.get('country')

        # Address validation logic
        if not street_address or not city or not postal_code or not country:
            messages.error(request, "All address fields are required.")
        elif len(postal_code) > 10:
            messages.error(request, "Postal code cannot exceed 10 characters.")
        else:
            # If the validation passes, save the address or proceed to next step
            # You can store address details or process them as needed.
            # For now, we assume that the address is saved successfully.
            messages.success(request, "Address saved successfully.")

            # Redirect to payment gateway (for example, proceed to the payment page)
            return redirect('payment_gateway')

    return render(request, 'ecommerce_app/checkout.html', {
        'cart_item_details': cart_item_details,  # Updated variable to use cart_item_details
        'total': total_price,
    })

@login_required
def payment_gateway(request):
    return render(request, 'ecommerce_app/payment_gateway.html')


@login_required
def complete_payment(request):
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')

        # Process payment based on selected method
        if payment_method == 'debit_card':
            card_number = request.POST.get('card_number')
            expiry_date = request.POST.get('expiry_date')
            cvv = request.POST.get('cvv')
            # Simulate payment processing...

        elif payment_method == 'upi':
            upi_id = request.POST.get('upi_id')
            # Simulate UPI payment processing...

        elif payment_method == 'cod':
            # Simulate COD payment confirmation...
            pass

        # Create order and clear cart
        cart_items = Cart.objects.filter(user=request.user)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        order = Order.objects.create(user=request.user, total_price=total_price, completed=True)
        
        # Correctly add Cart instances to the order
        for item in cart_items:
            order.products.add(item)  # Add the Cart instance to the order
        
        cart_items.delete()  # Clear the cart after order is created

        return redirect('orders')

    return redirect('checkout')


@login_required
def orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'ecommerce_app/orders.html', {'orders': orders})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, "Invalid credentials. Please try again.")
    else:
        form = LoginForm()
    return render(request, 'ecommerce_app/login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'ecommerce_app/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')



def search_view(request):
    query = request.GET.get('q', '')
    products = Product.objects.all()
    
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query) | Q(category__name__icontains=query)
        )
    
    return render(request, 'ecommerce_app/home.html', {
        'products': products,
        'query': query
    })
