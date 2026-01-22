from django.urls import path
from . import views

app_name = "Booking"

urlpatterns = [
    path("", views.BookingView.as_view(),name="booking"),
    path("login/", views.SendOTPView.as_view(), name="send_otp"),
    path("verify-otp/", views.VerifyOTPView.as_view(), name="verify_otp"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("logout/", views.logout_view, name="logout"),
]
