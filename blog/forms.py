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
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full block rounded-lg border border-gray-300 px-4 py-3 placeholder-gray-400 focus:ring-2 focus:ring-indigo-400',
                'aria-label': 'Title'
            }),
            'body': forms.Textarea(attrs={
                'class': 'w-full block rounded-lg border border-gray-300 px-4 py-3 placeholder-gray-400 focus:ring-2 focus:ring-indigo-400',
                'aria-label': 'Body'
            }),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
             'body': forms.Textarea(attrs={
                'rows': 4, 
                'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 resize-none',
                'placeholder': 'Write your comment here...'
            })
        }
        
        