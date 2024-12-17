from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('register-event/<int:event_id>/', views.register_event, name='register_event'),
    path('download_ticket/<int:ticket_id>/', views.download_ticket, name='download_ticket'),  # Use the download_ticket function here
    path('payment-success/', views.payment_success, name='payment_success'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('delete_registration/<int:registration_id>/', views.delete_registration, name='delete_registration'),
    path('favorites/', views.favorites, name='favorites'),
    path('add_to_favorites/<int:event_id>/', views.add_to_favorites, name='add_to_favorites'),
]
