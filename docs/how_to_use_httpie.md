# Install httpie

```bash
pip install httpie
```

# How to use

### Login

```bash
http POST :8000/api/auth/token email=admin@example.com password=admin
```

Sample response:

```
HTTP/1.1 200 OK
Allow: POST, OPTIONS
Set-Cookie: refresh=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4MTIyMTAyMSwiaWF0IjoxNjgxMTM0NjIxLCJqdGkiOiIxYTE2NDBmMDI1MGY0MDFmODc1Yjk0YmZlOGQ0YjU3MSIsInVzZXJfaWQiOjF9._AeHLX5th18fdKTpewv6WV_REZ-6XIDOdC4euZrZriQ; expires=Mon, 17 Apr 2023 13:50:21 GMT; HttpOnly; Max-Age=604800; Path=/; SameSite=None; Secure
Vary: Accept
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjgxMTM0OTIxLCJpYXQiOjE2ODExMzQ2MjEsImp0aSI6IjM0YWUwY2E1OTYzYzQ4YThiNmNkY2IwOWQ0ZGU2ZjA2IiwidXNlcl9pZCI6MX0.3uqr1zWeGRhIGxDnfq3eyOaXWosLRE5KOg08t06pnNc"
}

```

### Refresh token

```bash
http POST :8000/api/auth/refresh Cookie:refresh=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4MjE1ODIxMywiaWF0IjoxNjgxNTUzNDEzLCJqdGkiOiIzMDE5YmY4MWY1NWU0Y2YxODI0MGMyZGZjZGQwNmM1YyIsInVzZXJfaWQiOjF9.AgzXw9CWigu2-nsWMiMLUlk_hyL-6rVZE-Cf8NOlOGw
```

Response sample:

```
HTTP/1.1 200 OK
Allow: POST, OPTIONS
Set-Cookie: refresh=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4MTIyNDg5NCwiaWF0IjoxNjgxMTM4NDk0LCJqdGkiOiI3NmQzZjcyZTUxYmQ0OWEyYjVhNzI0YWRiNzlhNDI2YSIsInVzZXJfaWQiOjF9.JDHHXTGDtwJQ4HEo87m9XiFeaEkdnS3KG_g2aJtQt7w; expires=Mon, 17 Apr 2023 14:54:54 GMT; HttpOnly; Max-Age=604800; Path=/; SameSite=None; Secure
Vary: Accept
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjgxMTM4Nzk0LCJpYXQiOjE2ODExMzU2MTgsImp0aSI6IjMwMzY5M2E2ZjllZDQwNGI4YjcxN2JkYjhjY2EwZjYyIiwidXNlcl9pZCI6MX0.LT0hR8DdU1-jifgYRIvtcO8D09iFgovZWg8HSftMV4k"
}
```

### Register new user:

```bash
http POST :8000/api/user/register email=user1@example.com first_name=test last_name=user password=user1 password_confirm=user1
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
