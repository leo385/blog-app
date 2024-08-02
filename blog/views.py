from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic.list import ListView

from .models import Category, Post

# Create your views here.

class IndexView(ListView):
    
    template_name = "blog/index.html"
    context_object_name = "posts"

    def get_queryset(self):
        category_slug = self.kwargs.get("category_slug")
        
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            return Post.objects.filter(category=category)

        return Post.objects.all()

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        
        categories = Category.objects.exclude(name="no category")
        context["categories"] = categories
        
        return context




