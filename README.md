# 🔐 Shield Vault API

**Enterprise-Grade Zero-Trust Secure File Vault**  
Blyno Solutions | Backend Engineering Division

---

## 🚀 Overview

Shield Vault API is a high-security backend built for the Zero-Trust era.

It ensures:

- 🔐 AES-256 file encryption before storage
- ⏳ Time-limited secure file access
- 🛡️ JWT-based authentication & RBAC
- 🗄️ PostgreSQL-backed metadata storage
- 🔁 Automated database migrations via Alembic
- 🐳 Dockerized development & production environments

This project is structured using **Clean Architecture** principles to enforce scalability, security, and maintainability.

---

## 🧱 Tech Stack

| Layer             | Technology                  |
| ----------------- | --------------------------- |
| Framework         | FastAPI                     |
| Database          | PostgreSQL                  |
| ORM               | SQLAlchemy                  |
| Migrations        | Alembic                     |
| Security          | cryptography (AES-256), JWT |
| DevOps            | Docker & Docker Compose     |
| Testing           | Pytest                      |
| Static Analysis   | Ruff, Mypy                  |
| Security Scanning | Bandit, CodeQL              |

---

## 🏗 Project Structure

```

shield-vault-backend-api/
│
├── app/
│   ├── api/                # FastAPI routes
│   ├── application/        # Use cases
│   ├── domain/             # Core business logic
│   ├── infrastructure/     # DB & external integrations
│   ├── core/               # Config, DB setup, security
│   └── main.py             # Application entry point
│
├── alembic/                # Database migrations
├── docker/                 # Docker scripts
├── docker-compose.dev.yml
├── docker-compose.prod.yml
├── Dockerfile
└── .env

```

---

## 🧪 Running Locally (Development)

### 1️⃣ Start services

```bash
docker compose -f docker-compose.dev.yml up --build
```

### 2️⃣ Access API Docs

```
http://localhost:8000/docs
```

---

## 🔄 Database Migrations

Migrations run automatically via the dedicated migration container.

To create a new migration:

```bash
docker compose exec api alembic revision --autogenerate -m "message"
docker compose exec api alembic upgrade head
```

---

## 🛡 Security Philosophy

Shield Vault follows Zero-Trust principles:

- No plaintext file storage
- No hardcoded credentials
- Environment-driven configuration
- Strict CI checks
- Mandatory PR reviews
- Branch protection enabled

---

## 📦 Production Deployment

Production uses:

- Gunicorn + Uvicorn workers
- Dedicated migration container
- Environment-based secrets
- No exposed DB ports
- Hardened Docker configuration

---

## 📜 License

Proprietary - Blyno Solutions\
Unauthorized distribution is prohibited.

Unauthorized distribution is prohibited.
