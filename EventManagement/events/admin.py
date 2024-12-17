from django.contrib import admin
from .models import Event, Ticket  # Updated to import Ticket instead of EventRegistration

# Customize Event Admin
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'location', 'image')  # Display these fields in the list view
    list_filter = ('date', 'location')  # Add filters for date and location
    search_fields = ('name', 'description', 'location')  # Enable search by name, description, and location
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'date', 'location', 'image')
        }),
        ('Event Planning Details', {
            'fields': ('planning_image', 'planning_description')
        }),
        ('Event Management Details', {
            'fields': ('management_image', 'management_description')
        }),
        ('Event Technologies Details', {
            'fields': ('technologies_image', 'technologies_description')
        }),
        ('Pricing', {
            'fields': ('pricing',)
        }),
    )

# Customize Ticket Admin (previously EventRegistration)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'selected_section', 'amount_paid', 'purchase_date')  # Display relevant fields
    list_filter = ('purchase_date', 'event')  # Filter by purchase date and event
    search_fields = ('user__username', 'event__name')  # Search by user and event name
    # You can also add ordering if needed:
    # ordering = ('-purchase_date',)

# Register Models
admin.site.register(Event, EventAdmin)
admin.site.register(Ticket, TicketAdmin)  # Updated to use Ticket instead of EventRegistration
