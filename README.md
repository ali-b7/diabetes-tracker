![CI](https://github.com/ali-b7/diabetes-tracker/actions/workflows/ci.yml/badge.svg)



# Diabetes Tracking Web App

A simple web application that allows users to track:
- Blood glucose readings
- Insulin doses

## Tech Stack
- Python / Flask
- SQLite
- Flask-Login
- Pytest
- Ruff
- GitHub Actions (CI)

## Features
- User authentication
- Add and view glucose entries
- Add and view insulin entries
- Automated testing and linting on every push

## CI Pipeline
On every push or pull request:
1. Dependencies are installed
2. Code is linted with Ruff
3. Tests are executed with Pytest

If any step fails, the build is blocked.


I implemented a continuous integration pipeline using GitHub Actions.
Every push or pull request automatically installs dependencies, runs static code analysis with Ruff, and executes unit tests with Pytest.
If any step fails, the build is blocked, ensuring code quality and reliability

## Run locally (Windows)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py