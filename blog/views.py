from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
import json

from .models import Post, Comment, Like, User
from .forms import CommentForm, PostForm, CustomUserCreationForm


from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib import messages


class UserRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

from datetime import date, timedelta
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import Post, Comment, Like, Profile
from .forms import CommentForm, PostForm, CustomUserCreationForm

class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5
    def get_queryset(self):
        return Post.objects.filter(status='published')

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        post = self.get_object()
        is_premium = getattr(self.request, 'is_premium_user', False)
        ctx['is_premium'] = is_premium
        if post.access_level == 'premium' and not is_premium and post.author != self.request.user:
            ctx['paywall'] = True
            ctx['preview'] = post.body[:200] + '...'
        else:
            ctx['paywall'] = False
        ctx['comment_form'] = CommentForm()
        ctx['comments'] = post.comments.filter(parent__isnull=True)
        return ctx

class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post; form_class = PostForm; template_name = 'blog/post_form.html'
    def test_func(self): return self.request.user.role in ['author','admin']
    def form_valid(self, form):
        from django.utils.text import slugify
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post; form_class = PostForm; template_name = 'blog/post_form.html'
    def test_func(self): return self.request.user == self.get_object().author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post; template_name = 'blog/post_confirm_delete.html'; success_url = reverse_lazy('post_list')
    def test_func(self): return self.request.user == self.get_object().author

class SubscribeView(LoginRequiredMixin, TemplateView):
    template_name = 'blog/subscribe.html'

@login_required
@require_POST
def process_subscription(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    profile.is_subscribed = True
    profile.subscription_end_date = date.today() + timedelta(days=30)
    profile.save()
    messages.success(request, f"Subscribed until {profile.subscription_end_date:%b %d, %Y}")
    return redirect('post_list')

@login_required
@require_POST
def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)
    form = CommentForm(request.POST)
    if form.is_valid():
        c = form.save(commit=False); c.post=post; c.author=request.user; c.save()
        from asgiref.sync import async_to_sync
        from channels.layers import get_channel_layer
        cl = get_channel_layer()
        async_to_sync(cl.group_send)(f'comments_{slug}', {'type':'comment_message','comment':{
            'author':c.author.username,'body':c.body,'created_date':c.created_date.strftime('%b %d, %Y, %I:%M %p')
        }})
    return redirect('post_detail', slug=slug)

@login_required
@require_POST
def like_post(request, slug):
    post=get_object_or_404(Post,slug=slug)
    like,created=Like.objects.get_or_create(post=post,user=request.user)
    if not created: like.delete(); liked=False
    else: liked=True
    return JsonResponse({'liked':liked,'count':post.likes.count()})