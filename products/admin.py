from django.contrib import admin
from .models import Category, Product, Comment, Wishlist


class CommentInlines(admin.TabularInline):
    model = Comment
    fields = ['author', 'body', 'active', ]
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'datetime_created', ]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'category', 'datetime_created', 'active', ]

    inlines = [
        CommentInlines,
    ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'product', 'stars', 'datetime_created', 'active', ]


@admin.register(Wishlist)
class WishListAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'datetime_created']
