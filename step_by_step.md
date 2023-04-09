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
]

LOCAL_APPS = [
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
```

# Prepare dependencies for pip

```
mkdir -p requirements
touch requirements/{base,dev,test,prod}.txt
echo "-r base.txt" >! requirements/{dev,test,prod}.txt
echo "-r requirements/dev.txt" >! requirements.txt
echo "-r requirements/prod.txt" >! requirements_prod.txt
pip freeze >! requirements/base.txt
```
