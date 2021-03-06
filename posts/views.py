from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from .models import Post, Like, Comment
from profiles.models import Profile
from .forms import PostModelForm, CommentModelForm
from django.views.generic import UpdateView, DeleteView, DetailView, ListView, CreateView, FormView
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from braces.views import SelectRelatedMixin
from itertools import chain
from django.http import HttpResponseRedirect
# Create your views here.

@login_required
def friends_posts(request):
    profile = Profile.objects.get(user=request.user)
    # check who we are following
    users = [user for user in profile.friends.all()] 
    posts = []
    qs = None
    for one_user in users:
        prof = Profile.objects.get(user=one_user)
        prof_posts= prof.posts.all().filter()
        posts.append(prof_posts)
    if len(posts) >0:
        qs = sorted(chain(*posts), reverse=True, key=lambda obj: obj.created)

    context = {
        'posts': qs,
        'users': users,
    }
    return render(request, 'posts/friends_posts.html', context)


@login_required
def post_create(request):
    qs = Post.objects.all()
    profile = Profile.objects.get(user=request.user)
    post_form = PostModelForm()
    post_added = False

    if 'submit_post_form' in request.POST:
        post_form = PostModelForm(request.POST, request.FILES)
        if post_form.is_valid():
            instance = post_form.save(commit=False)
            instance.author = profile
            instance.save()
            post_form = PostModelForm()
            post_added = True

    context = {
        'qs': qs,
        'profile': profile,
        'post_form': post_form,
        'post_added': post_added,
    }
    return render(request, 'posts/post_form.html', context)

class PostDetail(FormMixin, DetailView):
    template_name = "posts/post_detail.html"
    model = Post
    form_class = CommentModelForm
    def get_success_url(self):
        return reverse('posts:single', kwargs={'pk': self.object.id})

    def get_initial(self):
       return {"post": self.get_object()}

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        profile = Profile.objects.get(user=request.user)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = profile
            instance.post = Post.objects.get(id=self.object.id)
            instance.save()
            form = CommentModelForm()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        return super(PostDetail, self).form_valid(form)


@login_required
def post_list_view(request):
    qs = Post.objects.all()
    profile = Profile.objects.get(user=request.user)

    context = {
        'qs': qs,
        'profile': profile,
    }
    return render(request, 'posts/main.html', context)


@login_required
def like_unlike_post(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id_like')
        post_obj = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)

        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)

        like, created = Like.objects.get_or_create(user=profile, post_id=post_id)

        if not created:
            if like.value=='Like':
                like.value='Unlike'
            else:
                like.value='Like'
        else:
            like.value='Like'

            post_obj.save()
            like.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/confirm_del.html'
    success_url = reverse_lazy('posts:all_posts')

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = Post.objects.get(pk=pk)
        if not obj.author.user == self.request.user:
            messages.warning(self.request, 'You need to be the author of the post in order to delete it')
        return obj

class PostUpdateView(LoginRequiredMixin, UpdateView):
    form_class = PostModelForm
    model = Post
    template_name = 'posts/update.html'
    #success_url = reverse_lazy('posts:all_posts')
    def get_success_url(self):
        return reverse('posts:single', kwargs={'pk': self.object.id})
        
    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        if form.instance.author == profile:
            return super().form_valid(form)
        else:
            form.add_error(None, "You need to be the author of the post in order to update it")
            return super().form_invalid(form)


# def comment_create_and_list_view(request):
#     qs = Post.objects.all()
#     profile = Profile.objects.get(user=request.user)
#     comment_form = CommentModelForm()

#     if 'submit_comment_form' in request.POST:
#         comment_form = CommentModelForm(request.POST)
#         if comment_form.is_valid():
#             instance = comment_form.save(commit=False)
#             instance.user = profile
#             instance.post = Post.objects.get(id=request.POST.get('post_id'))
#             instance.save()
#             comment_form = CommentModelForm()
#     context = {
#         'qs': qs,
#         'profile': profile,
#         'comment_form': comment_form,
#     }
#     return render(request, 'posts/main.html', context)