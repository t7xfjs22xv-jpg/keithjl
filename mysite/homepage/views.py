from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User 
from django.core.management import call_command
from .models import Post, Comment
from .forms import PostForm, SignUpForm

def landing_page(request):
    return render(request, 'blog/landing.html')

def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Set last_login to a real, valid current timestamp (no more nulls!)
            user.last_login = timezone.now()
            user.save()
            # Log the new user in automatically
            login(request, user)
            return redirect("create_post")
    else:
        form = UserCreationForm()
    return render(request, "blog/signup.html", {"form": form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('create_post')
    else:
        form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('landing')

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('blog_view')
    else:
        form = PostForm()
    return render(request, 'blog/create.html', {'form': form})

def blog_view(request):
    # Auto-fix for database tables on Render
    try:
        call_command('makemigrations', 'homepage', interactive=False)
        call_command('migrate', 'homepage', interactive=False)
    except Exception:
        pass

    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/blog.html', {'posts': posts})

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return JsonResponse({'likes_count': post.likes.count()})

def about_view(request):
    return render(request, 'blog/about.html')