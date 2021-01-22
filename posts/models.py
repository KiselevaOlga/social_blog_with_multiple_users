import misaka
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
# Create your models here.
# POSTS FILE MODELS
from django.urls import reverse
from groups.models import Group
from django.core.validators import FileExtensionValidator
import profiles.models

User = get_user_model()


class Post(models.Model):
    content = models.TextField()
    image = models.ImageField(upload_to='posts', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])], blank=True)
    liked = models.ManyToManyField('profiles.Profile', blank=True, related_name='likes')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE, related_name='posts', null=True) 
    #   message_html = models.TextField(editable=False)
    group = models.ForeignKey(Group, related_name='posts', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.content[:20])

    def num_likes(self):
        return self.liked.all().count()

    def num_comments(self):
        return self.comment_set.all().count()

    class Meta:
        ordering = ('-created',)

    def get_absolute_url(self):
        return reverse('posts:single', kwargs={'author': self.author, 'pk': self.pk})

class Comment(models.Model):
    user = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE, blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.pk)

LIKE_CHOICES=[
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
]

class Like(models.Model):
    user = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.user}-{self.post}-{self.value}'