from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Post
from .forms import PostForm
from django.urls import reverse_lazy
from .filters import PostFilter
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, PermissionDenied
from .models import Author
from django.contrib.auth.decorators import permission_required

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

class PostDetail(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "post.html"
    context_object_name = "post"

    raise_exception = True

    def get_queryset(self):
        self.queryset = Post.objects.filter(type_post="PO")
        return self.queryset

class PostCreate(PermissionRequiredMixin ,CreateView):
    form_class = PostForm
    model = Post
    template_name = "post_edit.html"
    permission_required = ('Models.add_post')
    raise_exception = True


    def form_valid(self, form):
        post = form.save(commit=False)
        post.type_post = 'PO'

        post.author_id = Author.objects.get(author=self.request.user)
        return super().form_valid(form)

class PostUpdate(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = "post_edit.html"
    permission_required = ('Models.change_post')

    raise_exception = True


    def get_queryset(self):
        self.queryset = Post.objects.filter(type_post="PO")
        post = self.get_object(queryset=self.queryset)
        if post.author_id != Author.objects.get(author=self.request.user):
            raise PermissionDenied
        return self.queryset

class PostDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = "post_delete.html"
    success_url = reverse_lazy("post_list")
    permission_required = ('Models.delete_post')

    raise_exception = True
    def get_queryset(self):
        self.queryset = Post.objects.filter(type_post="PO")
        post = self.get_object(queryset=self.queryset)
        if post.author_id != Author.objects.get(author=self.request.user):
            raise PermissionDenied
        return self.queryset

class ArticleCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('Models.add_post')

    raise_exception = True

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type_post = 'AR'
        post.author_id = Author.objects.get(author=self.request.user)
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

class ArticleDetail(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "post.html"
    context_object_name = "post"

    raise_exception = True

    def get_queryset(self):
        self.queryset = Post.objects.filter(type_post="AR")
        return self.queryset


class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = "post_edit.html"
    permission_required = ('Models.change_post')

    raise_exception = True

    def get_queryset(self):
        self.queryset = Post.objects.filter(type_post="AR")
        post = self.get_object(queryset=self.queryset)
        if post.author_id != Author.objects.get(author=self.request.user):
            raise PermissionDenied
        return self.queryset


class ArticleDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = "post_delete.html"
    success_url = reverse_lazy("post_list")
    permission_required = ('Models.delete_post')

    raise_exception = True

    def get_queryset(self):
        self.queryset = Post.objects.filter(type_post="AR")
        post = self.get_object(queryset=self.queryset)
        if post.author_id != Author.objects.get(author=self.request.user):
            raise PermissionDenied

        return self.queryset

class ChoicePost(TemplateView):
    template_name = "choice.html"