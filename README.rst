============
django-blog
============

This is blog application, where you can create some posts in specific category,
either publish or modificate it from backoffice admin panel.

Quick start
-----------

1. Add "blog" to your INSTALLED_APPS setting like this:

    INSTALLED_APPS = [
        ...,
        "django_blog",
    ]

2. Include the blog URLconf in your project urls.py like this::

    path("blog/", include("django_blog.urls")),

3. Run ``python manage.py migrate`` to create the models.

4. Start the development server and visit the admin to create categories and posts.

5. Visit the ``/blog/`` URL to participate in the blog.
