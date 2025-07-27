from django.urls import path
from .views import create_checkout_session, StripeWebhookView
from django.http import HttpResponse

urlpatterns = [
    path("buy/<uuid:course_uuid>/", create_checkout_session, name="buy-course"),
    path("webhooks/", StripeWebhookView.as_view(), name="stripe-webhook"),
    path("success/", lambda r: HttpResponse("Payment succeeded!")),
    path("cancel/",  lambda r: HttpResponse("Payment cancelled.")),
]