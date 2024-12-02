from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import HomeView, AvailableJobsView, ApplicationFormView, ContactView, LoginView, ThankYouView, RegisterView, AppliedJobsView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('available_jobs/', AvailableJobsView.as_view(), name='available_jobs'),
    path('apply/<int:job_id>/', ApplicationFormView.as_view(), name='apply'),
    path('applied_jobs/', AppliedJobsView.as_view(), name='applied_jobs'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('thank-you/', ThankYouView.as_view(), name='thank_you'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]
