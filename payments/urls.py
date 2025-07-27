# payments/urls.py
from django.urls import path
from . import views
from django.http import HttpResponse
urlpatterns = [
    path('buy/<uuid:course_uuid>/', views.create_checkout_session, name='buy-course'),
    path('webhooks/stripe/', views.StripeWebhookView.as_view(), name='stripe-webhook'),
    path('success/', lambda r: HttpResponse('Payment succeeded!')),
    path('cancel/',  lambda r: HttpResponse('Payment cancelled.')),
]