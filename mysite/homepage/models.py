from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    # The 'user' is the author; if the user is deleted, their posts are too.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    
    # Categories for the library: Love, Pain, Hope, Youth, Dreams, Life
    category = models.CharField(max_length=50, blank=True, null=True)
    
    # Track the 'ink' or appreciation for the work
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.user.username}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"