# Vscode

## Extensions:

### For Common Editor

- `VisualStudioExptTeam.vscodeintellicode`: IntelliCode
- `oderwat.indent-rainbow` : Indent Rainbow
- `spmeesseman.vscode-taskexplorer`: Task Explorer

### For Python

- `ms-python.python`: Python Extensions Pack: Pylance and Jupyter support
- `ms-python.isort`: Import Organization support for python files

### For Database

- `cweijan.vscode-mysql-client2`: MySQL Client

### For Github

- `GitHub.copilot`: GitHub Copilot
- `GitHub.vscode-pull-request-github`: GitHub Pull Request

### For Devops:

- `ms-azuretools.vscode-docker`: Docker
- `ms-vscode-remote.remote-containers`: Dev Containers

## Settings:

### User Settings

```
{
    "python.testing.unittestEnabled": false,
    "python.testing.pytestEnabled": true,
    "python.analysis.typeCheckingMode": "basic",
    "python.linting.flake8Enabled": true,
    "python.linting.flake8Args": [
        "--max-line-length=120"
    ],
    "python.linting.pylintEnabled": false,
    "python.linting.enabled": false,
    "python.linting.banditEnabled": false,
    "python.linting.mypyEnabled": false,
    "python.formatting.autopep8Args": ["--max-line-length", "250", "--experimental"],
    "files.trimTrailingWhitespace": true,
    "files.insertFinalNewline": true,
    "python.analysis.autoImportCompletions": true,
    "editor.wordWrap": "off",
    "explorer.confirmDelete": false,
    "editor.renderWhitespace": "all",
    "[python]": {
        "editor.formatOnType": true
    },
    "editor.inlineSuggest.enabled": true,
    "python.analysis.inlayHints.functionReturnTypes": true,
    "python.analysis.inlayHints.pytestParameters": true,
    "python.analysis.inlayHints.variableTypes": true,
    "terminal.integrated.enableMultiLinePasteWarning": false,
    "python.terminal.activateEnvInCurrentTerminal": true,
    "editor.insertSpaces": true,
    "editor.tabSize": 4,
    "editor.detectIndentation": true
}

```

## Launch Server

File: `.vscode/launch.json`

```
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "dj runserver",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/manage.py",
            "args": [
                "runserver", "0.0.0.0:8000"
            ],
            "django": true,
            "justMyCode": false
        },
        {
            "name": "dj shell",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/manage.py",
            "args": [
                "shell"
            ],
            "django": true,
            "justMyCode": false
        },
        {
            "name": "dj migrate",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/manage.py",
            "args": [
                "migrate",
            ],
            "django": true,
            "justMyCode": false
        },
        {
            "name": "dj command",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/manage.py",
            "args": [
                "sample_cmd",
                "-sample_option"
            ],
            "django": true,
            "justMyCode": false
        },
        {
            "name": "Docker: Python - Django",
            "type": "docker",
            "request": "launch",
            "preLaunchTask": "docker-run: debug",
            "python": {
                "pathMappings": [
                    {
                        "localRoot": "${workspaceFolder}",
                        "remoteRoot": "/app"
                    }
                ],
                "projectType": "django"
            }
        }
    ]
}
```

## Tasks

File: `.vscode/tasks.json`

```
{
    "version": "2.0.0",
    "tasks": [
        {
            "type": "docker-build",
            "label": "docker-build",
            "platform": "python",
            "dockerBuild": {
                "tag": "djvuepearlbe:latest",
                "dockerfile": "${workspaceFolder}/Dockerfile",
                "context": "${workspaceFolder}",
                "pull": true
            }
        },
        {
            "type": "docker-run",
            "label": "docker-run: debug",
            "dependsOn": [
                "docker-build"
            ],
            "python": {
                "args": [
                    "runserver",
                    "0.0.0.0:8000",
                    "--nothreading",
                    "--noreload"
                ],
                "file": "manage.py"
            }
        }
    ]
}

```

# How to import/export

* Export extentions list
```
code --list-extensions > extensions.txt
```

* Import extentions list
```
xargs -a extensions.txt -I {} code --install-extension {}
```
