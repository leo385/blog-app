from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.utils import timezone
from django.core.paginator import Paginator

from .models import Category, Post

# Create your views here.

class PostDetailView(DetailView):

    model = Post
    template_name = "blog/detail.html"

    

class IndexView(ListView):

    paginate_by = 2

    template_name = "blog/index.html"
    context_object_name = "posts"

    def get_queryset(self):
        
        queryset = Post.objects.all()
        sorting_option = self.request.GET.get("sorting")

        if sorting_option == "by_date_asc":
            queryset = queryset.order_by("pub_date")
         
        if sorting_option == "by_date_desc":
            queryset = queryset.order_by("-pub_date")

        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        
        context["categories"] = Category.objects.exclude(name="no category")

        sorting_option = self.request.GET.get("sorting", "")
        context["sorting"] = sorting_option

        category_slug = self.kwargs.get("category_slug")
        
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)

            posts = Post.objects.filter(category=category)

            if sorting_option == "by_date_asc":
                posts = posts.order_by("pub_date")
            
            if sorting_option == "by_date_desc":
                posts = posts.order_by("-pub_date")
            
            context["posts"] = posts

            paginator = Paginator(posts, 2)

            page_number = self.request.GET.get("page")
            page_obj = paginator.get_page(page_number)

            context["page_obj"] = page_obj

        else:
            context["posts"] = self.get_queryset()
            
            posts = self.get_queryset()

            paginator = Paginator(posts, 2)

            page_number = self.request.GET.get("page")
            page_obj = paginator.get_page(page_number)

            context["page_obj"] = page_obj


        return context

    
    def post(self, request, *args, **kwargs):
        
        sorting_option = request.POST.get('sorting')

        if sorting_option:
            # Przekierowanie z parametrem sorting
            if 'category_slug' in self.kwargs:
                category_slug = self.kwargs['category_slug']
                return redirect('{}?sorting={}'.format(
                    reverse('blog:category_detail', kwargs={'category_slug': category_slug}),
                    sorting_option))
            else:
                return redirect('{}?sorting={}'.format(
                    reverse('blog:index'),
                    sorting_option))

        return super().get(request, *args, **kwargs)


