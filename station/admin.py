from django.contrib import admin
from station.models import Bus, Ticket, Trip, Facility, Order


class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (TicketInline,)


admin.site.register(Bus)
admin.site.register(Ticket)
admin.site.register(Facility)
admin.site.register(Trip)
