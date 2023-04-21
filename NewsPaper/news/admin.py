from django.contrib import admin
from .models import Post, Comment, Author, Category, PostCategory


# Register your models here.
admin.site.site_url = '/news'
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(PostCategory)
