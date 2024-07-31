from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView

from .models import Category, Post

# Create your views here.

class IndexView(ListView):
    
    template_name = "blog/index.html"
   
    def get_queryset(self):
        pass

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        categories = Category.objects.exclude(name="no category")

        context["categories"] = categories
        context["posts"] = Post.objects.all()

        return context
    
