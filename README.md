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

- [ ] Add `CommentReaction` model
- [ ] Add Follower-Followee relationship
- [ ] Include pagination information for related fields in each model
- [x] Paginate tweet results when querying for a user and include page info
- [ ] Paginate comments results when querying for a tweet and include page info
- [ ] Search for users
- [ ] Search for tweets
- [ ] Blacklist tokens on password update and when tokens are refreshed
- [ ] Include `sql` script to preload data
```bash
# psql -h 127.0.0.1 -d <db-name> -f path/to/sql/script
psql -h 127.0.0.1 -d drf_custom_user_model -f ./scripts/data.sql

# https://stackoverflow.com/questions/53702621/read-csv-file-in-sql
```

# Common Questions

- [What is the difference between `create` method in `views.py` vs `create` method in `serializers.py`](https://stackoverflow.com/questions/63630590/drf-create-method-in-viewset-or-in-serializer)

# Resources

- [Understanding Views in Django Rest Framework](https://testdriven.io/blog/drf-views-part-1/)

- [Creating a custom user model](https://testdriven.io/blog/django-custom-user-model/)

- [Implementing djangorestframework-simplejwt](https://medium.com/django-rest/django-rest-framework-jwt-authentication-94bee36f2af8)
