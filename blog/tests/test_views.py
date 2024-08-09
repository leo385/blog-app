from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.urls import reverse
from django.shortcuts import get_object_or_404
import datetime

from blog.models import Category, Post

# Views test

def create_category(name):
    return Category.objects.create(name=name)

def create_post(category, title, pub_date):
    return Post.objects.create(category=category, title=title, pub_date=pub_date)

class IndexViewTests(TestCase):

    def setUp(self):
        self.category = create_category("test_category")
        self.category_slug = get_object_or_404(Category, slug=self.category.slug)
        self.url = reverse("blog:category_detail", args=(self.category_slug,))

        
        # For sorting goal
        self.category_foo = create_category("foo_category")
        self.category_foo_slug = get_object_or_404(Category, slug=self.category_foo.slug)

        self.post1 = create_post(self.category_foo, "abcd", pub_date="2024-08-01")
        self.post2 = create_post(self.category_foo, "abcdef", pub_date="2024-08-03")
        self.post3 = create_post(self.category_foo, "abcdefghi", pub_date="2024-08-05")


    def test_category_exists(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_category_not_exists(self):
        not_existing_cat = "abcd"
        url = reverse("blog:category_detail", args=(not_existing_cat,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_no_categories(self):
        self.category.delete()
        self.category_foo.delete()

        response = self.client.get(reverse("blog:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There aren't categories.")
        self.assertQuerySetEqual(response.context["categories"], [])

    def test_no_posts(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There aren't posts.")
        self.assertQuerySetEqual(response.context["posts"], [])
    
    def test_redirects_sorting_posts_by_date_asc(self): 
        
        # on index page
        response = self.client.post(reverse("blog:index"), {"sorting" : "by_date_asc"})
        self.assertRedirects(response, "/blog/?sorting=by_date_asc")

        # on category page
        response = self.client.post(reverse("blog:category_detail", kwargs={"category_slug" : self.category_foo_slug}), {"sorting" : "by_date_asc"})
        expected_url = reverse("blog:category_detail", kwargs={"category_slug" : self.category_foo_slug}) + "?sorting=by_date_asc"
        self.assertRedirects(response, expected_url)

    def test_index_page_sorting_posts_by_date_asc(self):
        
        response = self.client.get(reverse("blog:index") + "?sorting=by_date_asc")
        posts = list(response.context['posts'])

        self.assertEqual(posts, [self.post1, self.post2, self.post3])
    
    def test_category_page_sorting_posts_by_date_asc(self):

        response = self.client.get(reverse("blog:category_detail", kwargs={"category_slug" : self.category_foo_slug}) + "?sorting=by_date_asc")
        posts = list(response.context['posts'])

        self.assertEqual(posts, [self.post1, self.post2, self.post3])


    def test_redirects_sorting_posts_by_date_desc(self): 
        
        # on index page
        response = self.client.post(reverse("blog:index"), {"sorting" : "by_date_desc"})
        self.assertRedirects(response, "/blog/?sorting=by_date_desc")

        # on category page
        response = self.client.post(reverse("blog:category_detail", kwargs={"category_slug" : self.category_foo_slug}), {"sorting" : "by_date_desc"})
        expected_url = reverse("blog:category_detail", kwargs={"category_slug" : self.category_foo_slug}) + "?sorting=by_date_desc"
        self.assertRedirects(response, expected_url)

    def test_index_page_sorting_posts_by_date_desc(self):
        
        response = self.client.get(reverse("blog:index") + "?sorting=by_date_desc")
        posts = list(response.context['posts'])

        self.assertEqual(posts, [self.post3, self.post2, self.post1])
    
    def test_category_page_sorting_posts_by_date_desc(self):

        response = self.client.get(reverse("blog:category_detail", kwargs={"category_slug" : self.category_foo_slug}) + "?sorting=by_date_desc")
        posts = list(response.context['posts'])

        self.assertEqual(posts, [self.post3, self.post2, self.post1])
