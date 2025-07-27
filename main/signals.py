from django.dispatch import receiver
from allauth.account.signals import user_logged_in
from .models import UserProfile
SESSION_CATEGORY_KEY = "onboarding_category"
@receiver(user_logged_in)
def create_profile_on_first_google_login(sender, request, user, **kwargs):
    category = request.session.pop(SESSION_CATEGORY_KEY, None)
    if category:
        UserProfile.objects.get_or_create(
        user=user,
        defaults={"category": category}
    )