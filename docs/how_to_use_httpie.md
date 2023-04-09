# How to login:

```bash
http POST :8000/api/token email=admin@example.com password=admin
```

Sample response:

```
HTTP/1.1 200 OK
Allow: POST, OPTIONS
Content-Length: 483
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin
Date: Sun, 09 Apr 2023 15:48:42 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.10.5
Vary: Accept
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjgxMDU1NjIyLCJpYXQiOjE2ODEwNTUzMjIsImp0aSI6IjdkYWE2M2YzYWJhZTQ2NjFiYzQ5MDFhZDViNjJjNmQ4IiwidXNlcl9pZCI6MX0.E7iJNiBCBY7UZKwzgKJPvMYxXT6lOHPrOJHwAwOGDFU",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4MTE0MTcyMiwiaWF0IjoxNjgxMDU1MzIyLCJqdGkiOiI4ZTNkNWE4MWQzZGM0ZWQ3OWZmOTNlY2M3ODdlY2ZmOSIsInVzZXJfaWQiOjF9.LYuuOe0SzTyQWKcMcuIlZVNVX70xYUQHkC1iXh3E8jc"
}
```
