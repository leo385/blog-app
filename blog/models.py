from django.db import models 
from .validation import validate_only_letters 

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200, validators=[validate_only_letters])

    def __str__(self):
        return self.name


def get_or_create_default_category():
    category = Category.objects.get_or_create(name="no category")
    return category.index


class Post(models.Model):
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, default=get_or_create_default_category)

    image = models.ImageField(upload_to="images/", default="images/default_image.png")

    title = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.title

    def get_image_url(self):
        return f"{self.image.url}"
