# Django REST Framework with PostgreSQL and Simple JWT

An experiment on Django REST Framework with PostgreSQL and Simple JWT.

**Key Implementations:**
- Custom user model by modifying `Django`'s default user model and set `email` as `USERNAME_FIELD` instead of the default `username`
- Nested routing with [`drf-nested-routers`](https://github.com/alanjds/drf-nested-routers)
- Authentication with [`djangorestframework-simplejwt`](https://github.com/jazzband/djangorestframework-simplejwt)
- Class based views
- A user can only have 1 reaction to a tweet but reaction can be changed

**Models**
- User
- Tweet
- Comment
- TweetReaction

**Relationships between models**

- A `User` can have many `Tweet`s
- A `Tweet` can have many `Comment`s
- A `Tweet` can have many `TweetReaction`s

# Getting started

TBC

# Todos

- Blacklist tokens on password update and when tokens are refreshed

# Common Questions

- [What is the difference between `create` method in `views.py` vs `create` method in `serializers.py`](https://stackoverflow.com/questions/63630590/drf-create-method-in-viewset-or-in-serializer)

# Resources

- [Understanding Views in Django Rest Framework](https://testdriven.io/blog/drf-views-part-1/)

- [Creating a custom user model](https://testdriven.io/blog/django-custom-user-model/)

- [Implementing djangorestframework-simplejwt](https://medium.com/django-rest/django-rest-framework-jwt-authentication-94bee36f2af8)
