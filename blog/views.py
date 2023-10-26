from django.shortcuts import render
from django.views import generic
from .models import Post


class PostListView(generic.ListView):
    template_name = 'blog/posts_list.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        return Post.objects.filter(status='pub').order_by('datetime_created')


class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
