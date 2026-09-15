from django.contrib import admin
from .models import Profile, ServiceBooking, Vehicle


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ("registration_number", "make", "model", "owner", "year")
    search_fields = ("registration_number", "make", "model", "owner__username")


@admin.register(ServiceBooking)
class ServiceBookingAdmin(admin.ModelAdmin):
    list_display = ("id", "vehicle", "service_type", "preferred_date", "status", "estimated_cost")
    list_filter = ("status", "service_type")
    search_fields = ("vehicle__registration_number", "vehicle__owner__username")
    list_editable = ("status", "estimated_cost")


admin.site.register(Profile)
