from django.urls import path
from . import views
app_name = "main"
urlpatterns = [
path("get-started/", views.category_picker, name="category_picker"),
path("redirect/", views.redirect_after_login, name="redirect_after_login"),
path("dashboard/", views.dashboard, name="dashboard")
]