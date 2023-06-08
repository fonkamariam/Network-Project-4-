
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("following", views.following, name="following"),
    path("edit/<int:x>", views.edit, name="edit"),
    path("like/<int:y>", views.like, name="like"),
    path("unlike/<int:y>", views.unlike, name="unlike"),
    path("follow", views.follow, name="follow"),
    path("unfollow", views.unfollow, name="unfollow"),
    path("<str:namee>", views.profile, name="profile")
]
