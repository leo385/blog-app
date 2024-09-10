from django.contrib import admin
from .models import Category, Post

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'custom_description', 'category')
    ordering = ['title']

    def custom_description(self, obj):
        return obj.get_excerpt()
    custom_description.short_description = "Description"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'custom_posts')
    ordering = ['name']

    def custom_posts(self, obj):
        return obj.posts_count()
    custom_posts.short_description = 'Posts count'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
