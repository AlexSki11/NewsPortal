from django_filters import FilterSet, DateTimeFilter, ModelMultipleChoiceFilter

from .models import Post, Category
from django.forms import DateTimeInput


class PostFilter(FilterSet):


    category_choice = ModelMultipleChoiceFilter(
        field_name='post_category',
        queryset=Category.objects.all(),
        label='Категория',


    )

    data_create = DateTimeFilter(
        field_name="data_create",
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={"type": 'datetime-local'},
        ),

    label="После даты"
    )


    class Meta:
        model = Post
        fields = {
            'header': ['icontains'],
            'text': ['icontains'],

        }