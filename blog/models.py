from django.db import models 
from django.utils import timezone
from .validation import validate_only_letters, validate_excluding_special_chars
import datetime


# Create your models here.

class Category(models.Model):

    name = models.CharField(max_length=200, validators=[validate_only_letters], unique=True)
    parent_category = models.ForeignKey('self',
                                        null=True,
                                        blank=True,
                                        on_delete=models.SET_NULL,
                                        related_name='subcategories')
    
    class Meta:
        constraints = [ models.UniqueConstraint(fields=['parent_category'], name='unique_parent_category') ]

    def __str__(self):
        return self.name



def get_or_create_default_category():
    category = Category.objects.get_or_create(name="no category")
    return category.index


class Post(models.Model):
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, default=get_or_create_default_category)

    image = models.ImageField(upload_to="images/", default="images/default_image.png")

    title = models.CharField(max_length=200, validators=[validate_excluding_special_chars])
    description = models.CharField(max_length=2000)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.title

    def get_image_url(self):
        return f"{self.image.url}"

    def was_published_recently(self):
        return timezone.now() - datetime.timedelta(days=1) <= self.pub_date <= timezone.now() 


