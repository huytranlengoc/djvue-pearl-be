# Create a virtual environment

```python
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
```

# Install Django

```python
pip install django==4.2
pip install djangorestframework==3.14.0
```

# Start a new project

```python
django-admin startproject core .
```

Structure:

```
├── core
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── manage.py
```

# Prepare setting files

Update file `core/settings.py`

```
import os
SECRET_KEY = os.environ.get("SECRET_KEY", "djvue-secret-key")
DEBUG = bool(int(os.environ.get("DEBUG", "1")))
```

Change settings to multiple environment files:

```bash
mkdir -p core/settings
mv core/settings.py core/settings/base.py
touch core/settings/__init__.py
touch core/settings/{development,test,staging,production}.py
echo "from .base import *  # noqa" >> core/settings/{development,test,staging,production}.py
```

Update file `core/settings/base.py` (add `.parent`)

```
BASE_DIR = Path(__file__).resolve().parent.parent.parent
```

Update `DJANGO_SETTINGS_MODULE` in file `manage.py`

```
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.development")
```

# Split installed apps

Update file `core/settings/base.py` like this:

```
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
]

LOCAL_APPS = [
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
```

# Split dependencies for pip

```
mkdir -p requirements
touch requirements/{base,dev,test,prod}.txt
echo "-r base.txt" >! requirements/{dev,test,prod}.txt
echo "-r requirements/dev.txt" >! requirements.txt
echo "-r requirements/prod.txt" >! requirements_prod.txt
pip freeze >! requirements/base.txt
```

# Dockerize backend environment

```
echo "gunicorn==20.1.0" >! requirements/base.txt
touch Dockerfile
touch docker-compose.yml
touch docker-compose.debug.yml
touch .dockerignore
```

In `Dockerfile`:

```
# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-slim

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
COPY requirements/ requirements/
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi"]

```

In `.dockerignore`:

```
**/__pycache__
**/.venv
**/.classpath
**/.dockerignore
**/.env
**/.git
**/.gitignore
**/.project
**/.settings
**/.toolstarget
**/.vs
**/.vscode
**/*.*proj.user
**/*.dbmdl
**/*.jfm
**/bin
**/charts
**/docker-compose*
**/compose*
**/Dockerfile*
**/node_modules
**/npm-debug.log
**/obj
**/secrets.dev.yaml
**/values.dev.yaml
LICENSE
README.md
```

In `docker-compose.yml`:

```
version: '3.4'

services:
  djvuepearlbe:
    image: djvuepearlbe
    build:
      context: .
      dockerfile: ./Dockerfile
    ports:
      - 8000:8000

```

In `docker-compose.debug.yml`:

```
version: '3.4'

services:
  djvuepearlbe:
    image: djvuepearlbe
    build:
      context: .
      dockerfile: ./Dockerfile
    command: ["sh", "-c", "pip install debugpy -t /tmp && python /tmp/debugpy --wait-for-client --listen 0.0.0.0:5678 manage.py runserver 0.0.0.0:8000 --nothreading --noreload"]
    ports:
      - 8000:8000
      - 5678:5678
```
# Create a new app named `api`

```
django-admin startapp api
```

Update `core/settings/base.py`:

```
LOCAL_APPS = [
  "api",
]
```

# Create a common model

```
mkdir -p api/models
mv api/models.py api/models/base.py
echo "from .base import BaseModel" >! api/models/__init__.py
```

Update `api/models/base.py`:

```
from django.conf import settings
from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        default=None,
        blank=True,
        editable=False,
        on_delete=models.SET_NULL,
        related_name="%(class)s_created_by",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        default=None,
        blank=True,
        editable=False,
        on_delete=models.SET_NULL,
        related_name="%(class)s_updated_by",
    )

    class Meta:
        abstract = True

```

* We add some common fields: `created_at`, `updated_at`, `created_by`, `updated_by` to track history of each record
