from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    # This dropdown matches your theme categories
    category = forms.ChoiceField(choices=[
        ('Love', 'Love'), ('Life', 'Life'), ('Hope', 'Hope'), 
        ('Youth', 'Youth'), ('Pain', 'Pain'), ('Dreams', 'Dreams'), ('Other', 'Other')
    ])
    
    class Meta:
        model = Post  # Fixed: Points to Post, not User
        fields = ['title', 'category', 'content']