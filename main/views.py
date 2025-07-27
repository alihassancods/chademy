from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .models import UserProfile
from .forms import CategoryForm
SESSION_CATEGORY_KEY = "onboarding_category"

@never_cache
def category_picker(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data["category"]
            request.session[SESSION_CATEGORY_KEY] = category
            return redirect("google_login")
    else:
        if request.user.is_authenticated:
            return redirect("main:dashboard")
        form = CategoryForm()
        return render(request, "main/category_picker.html", {"form": form})
# Create your views here.
@login_required
def redirect_after_login(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        # Shouldn’t normally happen, but handle gracefully
        return redirect("accounts:category_picker")
    if profile.category == "student":
        return redirect("student_dashboard")
    else:
        return redirect("teacher_dashboard")


@login_required
def dashboard(request):
    return render(request, "main/student_dashboard.html")