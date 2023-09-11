from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .forms import PostForm
from django.urls import reverse_lazy
from .filters import PostFilter
# Create your views here.

class PostsList(ListView):
    model = Post
    ordering = ["-data_create"]
    queryset = Post.objects.filter(type_post="PO")
    template_name = "posts.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class PostDetail(DetailView):
    model = Post
    template_name = "post.html"
    context_object_name = "post"

    def get_queryset(self):
        self.queryset = Post.objects.filter(type_post="PO")
        return self.queryset

class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = "post_edit.html"


    def form_valid(self, form):
        post = form.save(commit=False)
        post.type_post = 'PO'
        return super().form_valid(form)

class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = "post_edit.html"

    def get_queryset(self):
        self.queryset = Post.objects.filter(type_post="PO")
        return self.queryset

class PostDelete(DeleteView):
    model = Post
    template_name = "post_delete.html"
    success_url = reverse_lazy("post_list")

    def get_queryset(self):
        self.queryset = Post.objects.filter(type_post="PO")
        return self.queryset

class ArticleCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type_post = 'AR'
        return super().form_valid(form)

class ArticlesList(ListView):
    model = Post
    ordering = ["-data_create"]
    queryset = Post.objects.filter(type_post="AR")
    template_name = "posts.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class ArticleDetail(DetailView):
    model = Post
    template_name = "post.html"
    context_object_name = "post"



    def get_queryset(self):
        self.queryset = Post.objects.filter(type_post="AR")
        return self.queryset


class ArticleUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = "post_edit.html"

    def get_queryset(self):
        self.queryset = Post.objects.filter(type_post="AR")
        return self.queryset


class ArticleDelete(DeleteView):
    model = Post
    template_name = "post_delete.html"
    success_url = reverse_lazy("post_list")

    def get_queryset(self):
        self.queryset = Post.objects.filter(type_post="AR")
        return self.queryset
