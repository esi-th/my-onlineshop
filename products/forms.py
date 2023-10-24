from django import forms
from .models import Comment


class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body', 'stars', ]
        widgets = {
            "body": forms.Textarea(attrs={
                "rows": 10,
            }),
        }
