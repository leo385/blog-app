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

class IndexViewTests(TestCase):

    def setUp(self):
        self.category = create_category("test_category")
        self.category_slug = get_object_or_404(Category, slug=self.category.slug)
        self.url = reverse("blog:category_detail", args=(self.category_slug,))

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
        response = self.client.get(reverse("blog:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There aren't categories.")
        self.assertQuerySetEqual(response.context["categories"], [])

    def test_no_posts(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There aren't posts.")
        self.assertQuerySetEqual(response.context["posts"], [])
