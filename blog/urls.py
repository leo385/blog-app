from django.urls import path

from . import views

app_name = "blog"
urlpatterns = [

    path("", views.IndexView.as_view(), name="index"),
    path("category/<str:category_slug>/", views.IndexView.as_view(), name="category_detail"),
    path("<slug:slug>/", views.PostDetailView.as_view(), name="post_detail"),
]

