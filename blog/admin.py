from django.contrib import admin
from .models import Post, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    fields = ['author', 'body', 'post', 'active', ]
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'datetime_created', 'datetime_modified', 'status', ]
    inlines = [
        CommentInline,
    ]


@admin.register(Comment)
class PostCommentsAmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'datetime_created', 'datetime_modified', 'active', ]
