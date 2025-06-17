from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', login_required(views.PostListView.as_view()), name='post_list'),
    path('post/new/', login_required(views.PostCreateView.as_view()), name='post_create'),
    path('post/<slug:slug>/', login_required(views.PostDetailView.as_view()), name='post_detail'),
    path('post/<slug:slug>/update/', login_required(views.PostUpdateView.as_view()), name='post_update'),
    path('post/<slug:slug>/delete/', login_required(views.PostDeleteView.as_view()), name='post_delete'),
    path('subscribe/', login_required(views.SubscribeView.as_view()), name='subscribe'),
    path('subscribe/process/', login_required(views.process_subscription), name='process_subscription'),
    path('post/<slug:slug>/comment/', login_required(views.add_comment), name='add_comment'),
    path('api/post/<slug:slug>/like/', login_required(views.like_post), name='like_post'),
]