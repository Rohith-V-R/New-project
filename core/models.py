from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.user.get_username()


class Vehicle(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="vehicles")
    make = models.CharField(max_length=60)
    model = models.CharField(max_length=60)
    registration_number = models.CharField(max_length=20, unique=True)
    year = models.PositiveIntegerField()
    color = models.CharField(max_length=30, blank=True)
    mileage = models.PositiveIntegerField(default=0, help_text="Current odometer reading in km")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.make} {self.model} ({self.registration_number})"


class ServiceBooking(models.Model):
    class ServiceType(models.TextChoices):
        GENERAL = "GENERAL", "General service"
        OIL = "OIL", "Oil & filter change"
        BRAKES = "BRAKES", "Brake inspection"
        TYRES = "TYRES", "Tyre service"
        REPAIR = "REPAIR", "Repair / diagnostics"

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        CONFIRMED = "CONFIRMED", "Confirmed"
        IN_PROGRESS = "IN_PROGRESS", "In progress"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="bookings")
    service_type = models.CharField(max_length=20, choices=ServiceType.choices)
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    class Meta:
        ordering = ["-preferred_date", "-preferred_time"]

    def __str__(self):
        return f"#{self.pk} — {self.vehicle}"
