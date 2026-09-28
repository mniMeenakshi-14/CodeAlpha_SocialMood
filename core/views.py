from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Post, Comment


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("feed")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def feed(request):
    followed = request.user.profile.following.values_list("user", flat=True)
    posts = Post.objects.filter(author__in=list(followed) + [request.user.id])
    return render(request, "feed.html", {"posts": posts})


@login_required
def create_post(request):
    if request.method == "POST":
        text = request.POST.get("text", "").strip()
        if text:
            Post.objects.create(author=request.user, text=text)
    return redirect("feed")


@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return JsonResponse({"liked": liked, "count": post.likes.count()})


@login_required
def profile(request, username):
    owner = get_object_or_404(User, username=username)
    is_following = request.user.profile.following.filter(id=owner.profile.id).exists()
    return render(request, "profile.html", {
        "owner": owner,
        "posts": owner.posts.all(),
        "is_following": is_following,
        "followers_count": owner.profile.followers.count(),
        "following_count": owner.profile.following.count(),
    })


@login_required
def toggle_follow(request, username):
    target = get_object_or_404(User, username=username)
    me = request.user.profile
    if target != request.user:
        if me.following.filter(id=target.profile.id).exists():
            me.following.remove(target.profile)
        else:
            me.following.add(target.profile)
    return redirect("profile", username=username)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        text = request.POST.get("text", "").strip()
        if text:
            Comment.objects.create(post=post, author=request.user, text=text)
    return redirect("feed")


@login_required
def people(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, "people.html", {"users": users})