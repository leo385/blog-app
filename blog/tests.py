from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
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

