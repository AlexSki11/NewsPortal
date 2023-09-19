from django import forms
from .models import Post
from django.core.exceptions import ValidationError
from .models import Author
from django.http import request


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "post_category",
            "header",
            "text",
        ]


    def clean(self):
        cleaned_data = super().clean()
        header = cleaned_data.get("header")
        text = cleaned_data.get("text")
        if header == text:
            raise ValidationError("Заголовок и текст не должны повторяться")

        return cleaned_data

