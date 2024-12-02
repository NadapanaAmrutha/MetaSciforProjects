from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Job, Application

class LoginView(AuthLoginView):
    template_name = 'jobs/login.html'

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('available_jobs')
        else:
            messages.error(request, 'Invalid credentials or not registered. Please register first.')
            return render(request, self.template_name)

class RegisterView(View):
    def get(self, request):
        return render(request, 'jobs/register.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password == confirm_password:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, password=password)
                user.save()
                login(request, user)
                return redirect('available_jobs')
            else:
                messages.error(request, "Username already exists.")
        else:
            messages.error(request, "Passwords do not match.")
        
        return render(request, 'jobs/register.html')

class HomeView(View):
    def get(self, request):
        return render(request, 'jobs/home.html')

class AvailableJobsView(View):
    @method_decorator(login_required)
    def get(self, request):
        jobs = Job.objects.all()
        applied_jobs = Application.objects.filter(user=request.user).values_list('job_id', flat=True)
        return render(request, 'jobs/available_jobs.html', {'jobs': jobs, 'applied_jobs': applied_jobs})
    
    @method_decorator(login_required)
    def get(self, request):
        query = request.GET.get('q', '').strip()
        jobs = Job.objects.all()

        if query:
            jobs = jobs.filter(
                title__icontains=query
            ) | jobs.filter(
                company__icontains=query
            ) | jobs.filter(
                skills__icontains=query
            )

        applied_jobs = Application.objects.filter(user=request.user).values_list('job_id', flat=True)
        return render(request, 'jobs/available_jobs.html', {'jobs': jobs, 'applied_jobs': applied_jobs})

class ApplicationFormView(View):
    @method_decorator(login_required)
    def get(self, request, job_id):
        job = get_object_or_404(Job, id=job_id)
        if Application.objects.filter(user=request.user, job=job).exists():
            messages.warning(request, "You have already applied for this job.")
            return redirect('available_jobs')
        return render(request, 'jobs/application_form.html', {'job': job})

    @method_decorator(login_required)
    def post(self, request, job_id):
        job = get_object_or_404(Job, id=job_id)
        if not Application.objects.filter(user=request.user, job=job).exists():
            Application.objects.create(user=request.user, job=job)
            return redirect('thank_you')
        messages.warning(request, "You have already applied for this job.")
        return redirect('available_jobs')

class AppliedJobsView(View):
    @method_decorator(login_required)
    def get(self, request):
        applications = Application.objects.filter(user=request.user).select_related('job')
        return render(request, 'jobs/applied_jobs.html', {'applications': applications})

class ContactView(View):
    def get(self, request):
        return render(request, 'jobs/contact.html')

class ThankYouView(View):
    def get(self, request):
        return render(request, 'jobs/thank_you.html')

def logout_view(request):
    logout(request)
    return redirect('login')
