from django import forms
from .models import Comments


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['content']