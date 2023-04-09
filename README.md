# djvue-pearl-be

Backend for Django VueJs Boilterplate: A Project to practice and can be re-usable

Step by Step guidline in docs: [STEP_BY_STEP](./step_by_step.md)

# A backend stack
### Django

    - django-rest-framework
    - django
    - celery

# Dockerize

    - Backend
    - Redis
    - MySQL
    - RabbitMQ

# Tools

    - pip
    - poetry
    - pre-commit

# Command Tools

    - httpie

# Development Tools

    - vscode
    - chrome Extensions

# Install pre-commit

```bash
pip install --upgrade --no-cache-dir pre-commit
pip install --upgrade --no-cache-dir flake8
pre-commit install
pre-commit install --hook-type commit-msg
```

Configure pre-commit the same as [.pre-commit-config.yaml](./.pre-commit-config.yaml)

Run the first time:

```bash
pre-commit run --all-files
```

### Uninstallation pre-commit (in-case)

```bash
pre-commit uninstall
pre-commit uninstall --hook-type commit-msg
```
