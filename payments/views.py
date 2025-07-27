from django.shortcuts import render

# Create your views here.
# payments/views.py
import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from .models import Course, PaymentHistory

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': course.stripe_price_id,
            'quantity': 1,
        }],
        mode='payment',
        metadata={'course_id': course.id},
        success_url=request.build_absolute_uri('/payments/success/'),
        cancel_url=request.build_absolute_uri('/payments/cancel/'),
    )
    return redirect(session.url, code=303)

@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(View):
    def post(self, request):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except Exception:
            return HttpResponse(status=400)

        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            course_id = session['metadata']['course_id']
            course = get_object_or_404(Course, id=course_id)
            PaymentHistory.objects.create(
                course=course,
                email=session['customer_details']['email'],
                stripe_session_id=session['id'],
                status='completed'
            )
        return HttpResponse(status=200)