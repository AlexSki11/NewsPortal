from django import forms
from .models import Post
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "author_id",
            "post_category",
            "header",
            "text",
        ]

    def clean(self):
        cleaned_data = super().clean()
        header = cleaned_data.get("header")
        text = cleaned_data.get("text")
        print(23)
        if header == text:
            raise ValidationError("Заголовок и текст не должны повторяться")

        return cleaned_data

