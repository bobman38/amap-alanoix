from django import forms
from .models import *
from django.utils.html import escape

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'cols': 80, 'rows': 4}),
        }
