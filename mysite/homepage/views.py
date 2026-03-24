from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from .models import Post, Comment
from .forms import SignUpForm, PostForm, CommentForm

# 1. LANDING PAGE
def landing_page(request):
    return render(request, 'landing.html')

# 2. SIGNUP
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # This hashes the password correctly
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('create_post')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

# 3. LOGIN
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('create_post')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# 4. LOGOUT
def logout_view(request):
    logout(request)
    return redirect('landing_page')

# 5. CREATE POST (WRITING)
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
    return render(request, 'create.html', {'form': form})

# 6. BLOG WALL
def blog_view(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog.html', {'posts': posts})

# 7. READ FULL POST & COMMENT
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()
    return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'form': form})

# 8. ABOUT AUTHOR
def about_author(request):
    return render(request, 'about.html')