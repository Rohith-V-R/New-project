from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import BookingForm, ProfileForm, RegisterForm, VehicleForm
from .models import ServiceBooking, Vehicle


def home(request):
    return render(request, "home.html")


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Welcome to CareX! Your account is ready.")
        return redirect("dashboard")
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        user = authenticate(request, username=request.POST.get("username"), password=request.POST.get("password"))
        if user:
            login(request, user)
            destination = request.GET.get("next") or ("admin_dashboard" if user.is_staff else "dashboard")
            return redirect(destination)
        messages.error(request, "Invalid username or password.")
    return render(request, "login.html")


def logout_view(request):
    logout(request)
    messages.info(request, "You have been signed out.")
    return redirect("home")


@login_required
def dashboard(request):
    upcoming = ServiceBooking.objects.filter(vehicle__owner=request.user).exclude(status__in=["COMPLETED", "CANCELLED"])[:4]
    return render(request, "dashboard.html", {"upcoming": upcoming, "vehicle_count": request.user.vehicles.count(), "booking_count": upcoming.count()})


@login_required
def garage(request):
    return render(request, "garage.html", {"vehicles": request.user.vehicles.all()})


@login_required
def add_vehicle(request):
    form = VehicleForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        vehicle = form.save(commit=False)
        vehicle.owner = request.user
        vehicle.save()
        messages.success(request, "Vehicle added to your garage.")
        return redirect("garage")
    return render(request, "add_vehicle.html", {"form": form})


@login_required
def book_service(request):
    form = BookingForm(request.POST or None, user=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Your service request has been submitted.")
        return redirect("bookings")
    return render(request, "book_service.html", {"form": form})


@login_required
def bookings(request):
    items = ServiceBooking.objects.filter(vehicle__owner=request.user).exclude(status="COMPLETED")
    return render(request, "bookings.html", {"bookings": items})


@login_required
def booking_details(request, pk):
    booking = get_object_or_404(ServiceBooking, pk=pk, vehicle__owner=request.user)
    return render(request, "booking_details.html", {"booking": booking})


@login_required
def history(request):
    items = ServiceBooking.objects.filter(vehicle__owner=request.user, status="COMPLETED")
    return render(request, "history.html", {"bookings": items})


@login_required
def profile(request):
    form = ProfileForm(request.POST or None, instance=request.user.profile)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Profile updated.")
        return redirect("profile")
    return render(request, "profile.html", {"form": form})


staff_required = user_passes_test(lambda u: u.is_staff)


@staff_required
def admin_dashboard(request):
    return render(request, "admin/dashboard.html", {
        "booking_count": ServiceBooking.objects.count(), "user_count": User.objects.count(),
        "pending_count": ServiceBooking.objects.filter(status="PENDING").count(),
        "recent": ServiceBooking.objects.select_related("vehicle", "vehicle__owner")[:8],
    })


@staff_required
def admin_bookings(request):
    items = ServiceBooking.objects.select_related("vehicle", "vehicle__owner").all()
    if request.method == "POST":
        booking = get_object_or_404(ServiceBooking, pk=request.POST.get("booking_id"))
        booking.status = request.POST.get("status", booking.status)
        booking.estimated_cost = request.POST.get("estimated_cost", booking.estimated_cost)
        booking.save()
        messages.success(request, f"Booking #{booking.pk} updated.")
        return redirect("admin_bookings")
    return render(request, "admin/bookings.html", {"bookings": items, "statuses": ServiceBooking.Status.choices})


@staff_required
def admin_users(request):
    users = User.objects.filter(is_staff=False, is_superuser=False).annotate(
        vehicle_total=Count("vehicles"), booking_total=Count("vehicles__bookings")
    )
    return render(request, "admin/users.html", {"users": users})
