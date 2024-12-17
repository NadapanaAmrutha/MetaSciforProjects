from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Event, Ticket
from .forms import UserRegistrationForm
import uuid
from weasyprint import HTML
from django.contrib.auth.mixins import LoginRequiredMixin

def event_list(request):
    events = Event.objects.all().order_by('date')
    return render(request, 'events/event_list.html', {'events': events})

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'events/event_detail.html', {'event': event})

@login_required
def register_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        selected_section = request.POST.get('section')
        num_tickets = int(request.POST.get('num_tickets', 1))  
        
        
        price = event.get_price(selected_section)  
        
        if not selected_section or price is None:
            return render(request, 'events/register_event.html', {
                'event': event,
                'error': 'Invalid section or pricing issue.'  
            })
        
        
        ticket_number = str(uuid.uuid4())[:8]
        
        ticket = Ticket.objects.create(
            user=request.user,
            event=event,
            selected_section=selected_section,
            num_tickets=num_tickets,
            amount_paid=price * num_tickets,
            ticket_number=ticket_number,
        )

        return render(request, 'events/ticket_details.html', {
            'event': event,
            'ticket': ticket,
            'total_price': price * num_tickets,
        })

    return render(request, 'events/register_event.html', {'event': event})

@login_required
def generate_ticket_pdf(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    
    html_content = render(request, 'events/ticket_pdf.html', {
        'ticket': ticket,
        'total_price': ticket.amount_paid  # Using the calculated amount_paid
    }).content

    pdf = HTML(string=html_content).write_pdf()

    
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ticket_{ticket.ticket_number}.pdf"'
    return response

@login_required
def download_ticket(request, ticket_id):
    
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    
    total_price = ticket.amount_paid  
    
    
    html_content = render(request, 'events/ticket_pdf.html', {
        'ticket': ticket,
        'total_price': total_price
    }).content
    
    
    pdf = HTML(string=html_content).write_pdf()

    
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ticket_{ticket.ticket_number}.pdf"'
    return response

@login_required
def payment_success(request):
    return render(request, 'events/payment_success.html')

@login_required
def dashboard(request):
    registrations = Ticket.objects.filter(user=request.user)  # Changed to Ticket model
    return render(request, 'events/dashboard.html', {'registrations': registrations})

def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'events/register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('event_list')
        else:
            return render(request, 'events/login.html', {'error': 'Invalid credentials'})
    return render(request, 'events/login.html')

def logout_user(request):
    logout(request)
    return redirect('login')

@login_required
def delete_registration(request, registration_id):
    registration = get_object_or_404(Ticket, id=registration_id, user=request.user)
    
    if request.method == 'POST':
        registration.delete()
        return redirect('dashboard')  # Redirect back to the dashboard after deletion
    
def event_list(request):
    # Get the search term from the GET request
    search_query = request.GET.get('search', '')
    
    # If there is a search query, filter events by name or description
    if search_query:
        events = Event.objects.filter(
            name__icontains=search_query
        ).order_by('date')
    else:
        events = Event.objects.all().order_by('date')
    
    return render(request, 'events/event_list.html', {'events': events})


@login_required
def add_to_favorites(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    # Toggle the event as a favorite
    if event in request.user.favorite_events.all():
        request.user.favorite_events.remove(event)
    else:
        request.user.favorite_events.add(event)
    return redirect('event_list')  # Redirect to event list after action

@login_required
def favorites(request):
    return render(request, 'events/favorites.html', {'user': request.user})

