from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.PublicSignupView.as_view(), name="register"),
    path("register/<uuid:token>/", views.InviteSignupView.as_view(), name="invite-register"),
]
