from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ["post"]
        labels = {
            "username": "Name",
            "email": "Email",
            "text": "Comment"
        }
        