from django.db import IntegrityError
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse
from django.views import generic
from .models import Group, GroupMember
from django.shortcuts import get_object_or_404
from django.contrib import messages
from profiles.models import Profile

class CreateGroup(LoginRequiredMixin, generic.CreateView):
    fields = ('name', 'description')
    model = Group

class SingleGroup(generic.DetailView):
    model = Group


class ListGroup(generic.ListView):
    model = Group


class JoinGroup(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single', kwargs={'slug': self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group, slug=self.kwargs.get('slug'))
        profile = Profile.objects.get(user=request.user)
        try:
            GroupMember.objects.create(user=profile, group=group)
        except IntegrityError :
             messages.warning(self.request,'Warning already a member')
        else:
            messages.success(self.request, 'You are now a member!')
        return super().get(request, *args, **kwargs)


class LeaveGroup(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single', kwargs={'slug': self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        try:
            membership = GroupMember.objects.filter(user=profile, group__slug=self.kwargs.get('slug')).get()
        except GroupMember.DoesNotExist:
            messages.warning(self.request, "Sorry, you are not in this group")
        else:
            membership.delete()
            messages.success(self.request, "You have left the group")
        return super().get(request, *args, **kwargs)



