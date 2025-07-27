# payments/urls.py
from django.urls import path
from . import views
urlpatterns = [
    path('buy/<int:course_id>/', views.create_checkout_session, name='buy-course'),
    path('webhooks/stripe/', views.StripeWebhookView.as_view(), name='stripe-webhook'),
    path('success/', lambda r: HttpResponse('Payment succeeded!')),
    path('cancel/',  lambda r: HttpResponse('Payment cancelled.')),
]