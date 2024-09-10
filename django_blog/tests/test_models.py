from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
import datetime

from blog.models import Category, Post


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


def create_user(username):
    return User.objects.create_user(username=username, password="password123")


class PostModelTests(TestCase):

    def setUp(self):
        User.objects.all().delete()
        self.category = Category.objects.create(name="no category")
        self.author = create_user("test")

    def tearDown(self):
        User.objects.all().delete()

    def test_title_is_valid(self):
    
       instance = Post(category=self.category, title="abcd", description="abcd", pub_date=timezone.now(), author=self.author)
       instance.full_clean()

    def test_title_is_invalid(self):

       instance = Post(category=self.category, title="abcd|", description="abcd", pub_date=timezone.now(), author=self.author)
       with self.assertRaises(ValidationError):
           instance.full_clean()

    def test_slug_is_not_empty(self):
        post = Post.objects.create(category=self.category, title="test post", slug="", pub_date=timezone.now(), author=self.author)
        self.assertNotEqual(post.slug, "", "Slug field is empty")

    def test_was_published_recently(self):
        instance = Post(category=self.category, title="abcd", description="abcd", pub_date=timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59), author=self.author)
        self.assertIs(instance.was_published_recently(), True) 

    def test_published_in_past(self):
        past_time = timezone.now() - datetime.timedelta(days=1)
        instance = Post(category=self.category, title="abcd", description="abcd", pub_date=past_time, author=self.author)
        self.assertIs(instance.was_published_recently(), False) 
    
    def test_published_in_future(self):
        future_time = timezone.now() + datetime.timedelta(seconds=1)
        instance = Post(category=self.category, title="abcd", description="abcd", pub_date=future_time, author=self.author)
        self.assertIs(instance.was_published_recently(), False)
