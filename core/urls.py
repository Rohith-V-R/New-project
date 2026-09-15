from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("garage/", views.garage, name="garage"),
    path("vehicles/add/", views.add_vehicle, name="add_vehicle"),
    path("book-service/", views.book_service, name="book_service"),
    path("bookings/", views.bookings, name="bookings"),
    path("bookings/<int:pk>/", views.booking_details, name="booking_details"),
    path("history/", views.history, name="history"),
    path("profile/", views.profile, name="profile"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("admin-bookings/", views.admin_bookings, name="admin_bookings"),
    path("admin-users/", views.admin_users, name="admin_users"),
]
