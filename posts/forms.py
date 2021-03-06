from django import forms
from .models import Post, Comment
from django.forms.widgets import HiddenInput

class PostModelForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea())
    class Meta:
        model = Post
        fields = ('content', 'image', 'group')


class CommentModelForm(forms.ModelForm):
    body = forms.CharField(label='', 
                            widget=forms.TextInput(attrs={'placeholder': 'Add a comment...'}))
    class Meta:
        model = Comment
        fields = ('body',)