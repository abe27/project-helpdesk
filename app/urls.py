from django.urls import path
from app import views

urlpatterns = [
    path("", views.dashboard.index),
    path("signin", views.auth.sign_in, name="signin"),
    path("signup", views.auth.sign_up, name="signup"),
    path("signout", views.auth.sign_out, name="signout"),
    path("form", views.form.form, name="form"),
    path("status", views.history.status, name="status"),
    path("status/admin", views.history.status_admin, name="status_admin"),
    path("assign_report", views.history.assign_report, name="assign_report"),
    path("status/staff", views.history.status_staff, name="status_staff"),
    path("accept_report", views.history.accept_report, name="accept_report"),
    path("complete_report", views.history.complete_report, name="complete_report"),
    path("user", views.user.index, name="user"),
    path("profile", views.profile.index, name="profile"),
    path("generate-report/", views.dashboard.generate_report, name="generate_report"),
]
