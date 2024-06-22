from django.urls import path , include
from . import views

app_name = 'accounts'
urlpatterns = [
    path("", views.home , name="home"),
    path("login", views.login_user, name='login'),
    path("logout", views.logout_user, name='logout'),
    path("register", views.register, name="register"),
    path("profile", views.profile, name="profile"),
    path("profile/edit", views.profile_edit, name='Edit_profile'),
    path("reset", views.reset, name="reset"),
]