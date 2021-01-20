from django.db import models
from django.utils.text import slugify
import misaka
from django.urls import reverse
# Create your models here.
#GROUPS FILE MODELS
from django import template
from django.contrib.auth import get_user_model
User = get_user_model()
register = template.Library()


class Group(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(null=True, unique=True)
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=False, default='', blank=True)
    members = models.ManyToManyField('profiles.Profile', through='GroupMember')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.description_html = misaka.html(self.description)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('groups:single', kwargs={'slug': self.slug})
    
    def get_users(self):
        users = []
        for member in self.members.all():
            users += [member.user]
        return users
    
    class Meta:
        ordering = ['name']


class GroupMember(models.Model):
    group = models.ForeignKey(Group, related_name='memberships',on_delete=models.CASCADE)
    user = models.ForeignKey('profiles.Profile', related_name='user_groups', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)
    
    def get_groups(self):
        self.group.all().count()

    class Meta:
        unique_together = ('group', 'user')
