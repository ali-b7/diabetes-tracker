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
