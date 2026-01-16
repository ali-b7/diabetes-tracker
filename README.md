![CI](https://github.com/ali-b7/diabetes-tracker/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.12-blue)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)



# Diabetes Tracking Web Application

This project is a simple web-based application used as a **case study to demonstrate the design and implementation of a CI/CD pipeline**.  
The application allows users to track blood glucose readings and insulin doses, while the primary focus of the project is on automated validation and reliable builds.

---

## Features

- User authentication
- Add and view blood glucose entries
- Add and view insulin entries
- Persistent data storage using SQLite
- Automated testing and linting on every push

---

## Tech Stack

- Python / Flask
- SQLite
- Flask-Login
- Pytest
- Ruff
- GitHub Actions (Continuous Integration)
- Docker & Docker Compose

---

## CI Pipeline

On every push or pull request, the following steps are executed automatically using **GitHub Actions**:

1. Dependencies are installed  
2. Static code analysis is performed using Ruff  
3. Automated tests are executed using Pytest  
4. If any step fails, the pipeline stops and the build is blocked  

This ensures that only validated code is allowed to proceed to the build stage.

---

## Running the Application Locally (Windows)

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py
