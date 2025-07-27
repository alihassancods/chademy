import stripe
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse

from .models import PaymentHistory
from videoplayer.models import Course

stripe.api_key = settings.STRIPE_SECRET_KEY
User = get_user_model()


def create_checkout_session(request, course_uuid):
    """
    Create a Stripe Checkout Session.
    URL:  /payments/buy/<uuid:course_uuid>/
    """
    course = get_object_or_404(Course, uuid=course_uuid)

    # Re-use price if we already created it
    if not course.stripe_price_id:
        product = stripe.Product.create(name=course.title)
        price = stripe.Price.create(
            unit_amount=int(float(course.price) * 100),
            currency="usd",
            product=product.id,
        )
        course.stripe_price_id = price.id
        course.save()

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{"price": course.stripe_price_id, "quantity": 1}],
        mode="payment",
        client_reference_id=str(request.user.id),      # who is paying
        metadata={"course_uuid": str(course.uuid)},    # what is bought
        success_url=request.build_absolute_uri("/payments/success/"),
        cancel_url=request.build_absolute_uri("/payments/cancel/"),
    )
    return redirect(session.url, code=303)


@method_decorator(csrf_exempt, name="dispatch")
class StripeWebhookView(View):
    """
    Handle Stripe webhooks.
    URL:  /payments/webhooks/
    """
    def post(self, request):
        payload = request.body
        sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except Exception:
            return HttpResponse(status=400)

        if event["type"] == "checkout.session.completed":
            stripe_session = event["data"]["object"]

            user_id = stripe_session.get("client_reference_id")
            course_uuid = stripe_session["metadata"]["course_uuid"]

            user = get_object_or_404(User, id=user_id)
            course = get_object_or_404(Course, uuid=course_uuid)

            # 1) Save the payment record
            PaymentHistory.objects.get_or_create(
                course=course,
                defaults={
                    "email": stripe_session["customer_details"]["email"],
                    "stripe_session_id": stripe_session["id"],
                    "status": "completed",
                },
            )

            # 2) Grant access
            course.accessibleBy.add(user)
            course.save()

        return HttpResponse(status=200)