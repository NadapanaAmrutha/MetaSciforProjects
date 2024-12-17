from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView



urlpatterns = [
    path('', views.home, name='home'),  # Home page showing products and categories
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),  # Product detail page
    path('cart/', views.cart, name='cart'),  # Cart page for logged-in users
    path('checkout/', views.checkout, name='checkout'),  # Checkout page for logged-in users
    path('payment-gateway/', views.payment_gateway, name='payment_gateway'),
    path('complete-payment/', views.complete_payment, name='complete_payment'),
    path('orders/', views.orders, name='orders'),  # Orders page showing user orders
    path('login/', views.login_view, name='login'),  # Login page for authentication
    path('signup/', views.signup_view, name='signup'),  # Signup page for new users
    path('search/', views.search_view, name='search'),  # Search functionality
    path('logout/', views.logout_view, name='logout'), # Logout view
    

    # Updated routes for cart actions (removed colons)
   path('cart/update/<int:product_id>/', views.update_quantity, name='update_quantity'),
path('cart/remove/<int:product_id>/', views.remove_item, name='remove_item'),

]
