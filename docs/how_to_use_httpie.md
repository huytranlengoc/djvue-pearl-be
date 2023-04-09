# Install httpie

```bash
pip install httpie
```

# How to use
### Register new user:

```bash
http POST :8000/api/register email=user1@example.com first_name=test last_name=user password=user1 password_confirm=user1
```

Sample response:
```
{
    "email": "user1@example.com",
    "first_name": "user1",
    "id": 2,
    "last_name": "user1"
}

```
### Login

```bash
http POST :8000/api/token email=admin@example.com password=admin
```

Sample response:

```
{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjgxMDU1NjIyLCJpYXQiOjE2ODEwNTUzMjIsImp0aSI6IjdkYWE2M2YzYWJhZTQ2NjFiYzQ5MDFhZDViNjJjNmQ4IiwidXNlcl9pZCI6MX0.E7iJNiBCBY7UZKwzgKJPvMYxXT6lOHPrOJHwAwOGDFU",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4MTE0MTcyMiwiaWF0IjoxNjgxMDU1MzIyLCJqdGkiOiI4ZTNkNWE4MWQzZGM0ZWQ3OWZmOTNlY2M3ODdlY2ZmOSIsInVzZXJfaWQiOjF9.LYuuOe0SzTyQWKcMcuIlZVNVX70xYUQHkC1iXh3E8jc"
}
```
