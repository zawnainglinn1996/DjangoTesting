from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from hello.models import Post
# for use Login action
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.template.defaultfilters import linebreaksbr
from django.http import HttpResponse
from operator import attrgetter
from users.views import get_block_queryset

posts = [
    {
        'author': "zaw naing linn",
        'title': "Blog1",
        'content': 'First Post Content',
        'date_posted': "August 27,2019"

    },
    {
        'author': "Lwin Mar Aung",
        'title': "Blog2",
        'content': 'Second Post Content',
        'date_posted': "July 2,2019"

    }
]


def home(request):
    context = {'posts': Post.objects.all()}
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    # <app>/<model>_<viewtype.html>
    context_object_name = 'posts'
    # for ascending or descending
    ordering = ['-date_posted']
    # for show only two page example 12345 etc
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user-post.html'
    # <app>/<model>_<viewtype.html>
    context_object_name = 'posts'
    # for ascending or descending
    ordering = ['-date_posted']
    # for show only two page example 12345 etc
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('date_posted')
    # for all user post show by click username or author
    # def get_query_set(self):
    # user = get_object_or_404(User, username=self.kwargs.get('username'))
    # return Post.objects.filter(author=user).ordery_by('date_posted')


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post-detail.html'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post-create.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/post-create.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post-delete.html'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


def home_screen_view(request):
    context = {}
    query=''
    if request.GET():
        query=request.GET('q')
        context['query']=str(query)

    blog_posts = sorted(get_block_queryset(query), key=attrgetter('date_updated'), reverse=True)
    context['blog_posts'] = blog_posts
    return render(request, 'blog/base.html', context)

# for Search Action

# Create your views here.
