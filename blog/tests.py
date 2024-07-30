from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone

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



