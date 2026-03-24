from django import forms
from .models import Post, Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm # <-- Add this

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'category', 'content']

# Use UserCreationForm instead of ModelForm
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username'] # Email and password are handled automatically