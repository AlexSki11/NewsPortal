from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Post
from .forms import PostForm
from django.urls import reverse_lazy
from .filters import PostFilter
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, PermissionDenied
from .models import Author, Category, Subscriptions
from django.contrib.auth.decorators import permission_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
#celery_task
from .tasks import create_post
from django.http import HttpResponseRedirect
from django.core.cache import cache
import logging
from django.http import HttpResponseServerError
# Create your views here.
logger = logging.getLogger(__name__)


class PostsList(ListView):
    model = Post
    ordering = ["-data_create"]
    queryset = Post.objects.filter(type_post="PO")
    template_name = "posts.html"
    context_object_name = "posts"
    paginate_by = 10
    
    def get_queryset(self):  
        logger.error("error")
        logger.critical('crit')
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

    def get_object(self, *args, **kwargs):

        obj = cache.get(f'post-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj

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
        post.save()
        post.post_category.set(form.data['post_category'])
        create_post.delay(post.id)

        return HttpResponseRedirect(post.get_absolute_url())


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
        post.save()
        post.post_category.set(form.data['post_category'])
        create_post.delay(post.id)

        return HttpResponseRedirect(post.get_absolute_url())



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

    def get_object(self, *args, **kwargs):

        obj = cache.get(f'post-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj


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

    def get(self, request, *args, **kwargs):
        return super().get(self, request, *args, **kwargs)

@login_required
@csrf_protect
def subscriptions(request):
    if request.method == "POST":
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id = category_id)
        action = request.POST.get('action')

        if action == "subscribe":
            Subscriptions.objects.create(user=request.user, category=category)
        elif action == "unsubscribe":
            Subscriptions.objects.filter(user=request.user, category=category).delete()

    category_with_subscriptions = Category.objects.annotate(user_subscribed=Exists(
                                Subscriptions.objects.filter(user=request.user,
                                                             category=OuterRef('pk'),)
    )).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': category_with_subscriptions},
    )

#Фун-я для проверки логов
def test(request):

    return HttpResponseServerError()

#celery
