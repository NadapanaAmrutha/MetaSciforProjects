from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    favorites = models.ManyToManyField(User, related_name='favorite_events', blank=True)

    # Detailed sections for Event Detail Page
    planning_image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    planning_description = models.TextField(null=True, blank=True)

    management_image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    management_description = models.TextField(null=True, blank=True)

    technologies_image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    technologies_description = models.TextField(null=True, blank=True)

    # Pricing for different sections
    pricing = models.JSONField(null=True, blank=True)  # Example: {"Gold Fan Zone": 10000, "Platinum Experience": 16500}

    def __str__(self):
        return self.name
    
    def get_price(self, section):
        """
        Retrieve the price for a given section from the pricing field.
        Returns None if the section is not found.
        """
        if self.pricing and section in self.pricing:
            return self.pricing.get(section)
        return None


class Ticket(models.Model):  # Replaces EventRegistration for consistency with "Ticket"
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    selected_section = models.CharField(max_length=200, default="General Admission")
    num_tickets = models.PositiveIntegerField(default=1)  # Added number of tickets
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    ticket_number = models.CharField(max_length=50, unique=True)  # Unique ticket identifier
    purchase_date = models.DateTimeField(auto_now_add=True)  # Renamed for consistency
    registered_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.event.name} - {self.selected_section}"
    
    

