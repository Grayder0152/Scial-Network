from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """User model addition"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_request = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    """Model for user`s posts"""
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(User, related_name="liked_posts")
    is_liked = models.BooleanField(default=False)
    title = models.CharField(max_length=50)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_likes(self):
        return self.liked_by.count()

    def __str__(self):
        return self.title


class LikeAnalytics(models.Model):
    """Model for like analytics"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    liked_time = models.DateField(auto_now=True)

    def __str__(self):
        return f"User '{self.user}' liked post '{self.post}' at {self.liked_time.strftime('%Y-%m-%d')}"
