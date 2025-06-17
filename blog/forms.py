from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Post, Comment

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'role',)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'featured_image', 'category', 'tags', 'status', 'access_level']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Join the discussion...'}),
        }