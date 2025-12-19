from django.urls import path
from . import views

app_name = "Booking"

urlpatterns = [
    path("",views.BookingView.as_view(),name="booking"),
    path("login/", views.send_otp, name="send_otp"),
    path("verify-otp/", views.verify_otp, name="verify_otp")
]
