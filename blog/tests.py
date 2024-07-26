from django.test import TestCase
from django.core.exceptions import ValidationError

from .models import Category


# Create your tests here.

class CategoryModelTests(TestCase):
    
    def test_category_is_valid(self):
        instance = Category(name="abcd")
        instance.full_clean()

    def test_category_is_invalid(self):
        instance = Category(name="abcd1234")
        with self.assertRaises(ValidationError):
            instance.full_clean()


