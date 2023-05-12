from django.contrib import admin
from .models import Post, Comment, Author, Category, PostCategory


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'type_news', 'post_rating')
    list_filter = ('title', 'author', 'type_news', 'post_rating')
    search_fields = ('title', 'author__username__username', 'text')


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('username', 'author_rating')
    search_fields = ('username__username',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_title',)
    search_fields = ('category_title',)


admin.site.site_url = '/news'
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(PostCategory)
