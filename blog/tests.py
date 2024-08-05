from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.urls import reverse
from django.shortcuts import get_object_or_404
import datetime

from .models import Category, Post



# Create your tests here.

class CategoryModelTests(TestCase):
    
    def test_category_is_valid(self):
        instance = Category(name="abcd")
        instance.full_clean()

    def test_category_is_invalid(self):
        instance = Category(name="abcd1234")
        with self.assertRaises(ValidationError):
            instance.full_clean()
    
    def test_slug_is_not_empty(self):
        category = Category.objects.create(name="test category", slug="")
        self.assertNotEqual(category.slug, "", "Slug field is empty")


class PostModelTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="no category")

    def test_title_is_valid(self):
    
       instance = Post(category=self.category, title="abcd", description="abcd", pub_date=timezone.now())
       instance.full_clean()

    def test_title_is_invalid(self):

       instance = Post(category=self.category, title="abcd|", description="abcd", pub_date=timezone.now())
       with self.assertRaises(ValidationError):
           instance.full_clean()

    def test_was_published_recently(self):
        instance = Post(category=self.category, title="abcd", description="abcd", pub_date=timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59))
        self.assertIs(instance.was_published_recently(), True) 

    def test_published_in_past(self):
        past_time = timezone.now() - datetime.timedelta(days=1)
        instance = Post(category=self.category, title="abcd", description="abcd", pub_date=past_time)
        self.assertIs(instance.was_published_recently(), False) 
    
    def test_published_in_future(self):
        future_time = timezone.now() + datetime.timedelta(seconds=1)
        instance = Post(category=self.category, title="abcd", description="abcd", pub_date=future_time)
        self.assertIs(instance.was_published_recently(), False) 


def create_category(name):
    return Category.objects.create(name=name)


# Views test

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


