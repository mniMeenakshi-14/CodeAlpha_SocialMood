from django.urls import path
from . import views

urlpatterns = [
    path("", views.feed, name="feed"),
    path("register/", views.register, name="register"),
    path("post/new/", views.create_post, name="create_post"),
    path("like/<int:post_id>/", views.toggle_like, name="toggle_like"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path("follow/<str:username>/", views.toggle_follow, name="toggle_follow"),
    path("comment/<int:post_id>/", views.add_comment, name="add_comment"),
    path("people/", views.people, name="people"),
]