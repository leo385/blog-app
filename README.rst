============
django-blog
============

This is blog application, where you can create some posts in specific category,
either publish or modificate it from backoffice admin panel.

You can check it out on my vps, here: https://frog02-20301.wykr.es/blog/

Quick start
-----------

1. Add "blog" to your INSTALLED_APPS setting like this:

    INSTALLED_APPS = [
        ...,
        "django_blog.apps.BlogConfig",
    ]

2. Include the blog URLconf in your project urls.py like this::

    path("blog/", include("django_blog.urls")),

3. Run ``python manage.py migrate`` to create the models.

4. Start the development server and visit the admin to create categories and posts.

5. Visit the ``/blog/`` URL to participate in the blog.

6. In root project directory, set in settings.py:

    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'

It is needed for images that were uploaded by post itself,
we need to separate images somewhere.

7. In the same directory, set in urls.py

    Add imports:
        from django.conf.urls.static import static
        from django.conf import settings

    and below urlpatterns = [], add static url pattern for media
        if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
