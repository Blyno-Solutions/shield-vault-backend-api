# 🏗 Shield Vault Architecture

Shield Vault follows Clean Architecture principles.

## 🧠 High-Level Flow

Client → API Layer → Application Layer → Domain Layer → Infrastructure → Database

---

## 📂 Layer Breakdown

### 1️⃣ API Layer (`app/api/`)

- FastAPI routers
- Request/Response validation
- HTTP concerns only
- No business logic

---

### 2️⃣ Application Layer (`app/application/`)

- Use cases
- Orchestrates domain logic
- Coordinates repositories
- Contains workflows

---

### 3️⃣ Domain Layer (`app/domain/`)

- Entities
- Repository interfaces
- Pure business rules
- No framework dependencies

This layer must remain pure.

---

### 4️⃣ Infrastructure Layer (`app/infrastructure/`)

- SQLAlchemy models
- Repository implementations
- External services (encryption, storage)
- Database communication

---

### 5️⃣ Core Layer (`app/core/`)

- Config
- Database session
- Security utilities
- Shared components

---

## 🔐 Encryption Flow (Planned)

```

Upload File
↓
Encrypt with AES-256
↓
Store encrypted binary
↓
Store metadata in PostgreSQL

```

Decryption only happens upon authorized request.

---

## 🗄 Database Migrations

Alembic is used for schema management.

Migrations are:

- Version-controlled
- Reversible
- Automatically executed via migration container

---

## 🐳 Container Strategy

Services:

- `db` → PostgreSQL
- `migrate` → Runs Alembic
- `api` → FastAPI app

API depends on successful migration.

---

## 🛡 Security Principles

- Zero-Trust
- Least Privilege
- No plaintext secrets
- Strict CI enforcement
- Mandatory code review

---

## 📈 Scalability Path

Future-ready for:

- Object storage (S3 / MinIO)
- Kubernetes deployment
- Horizontal scaling
- Background workers
- Rate limiting
- Audit logging

---

This architecture ensures:

- Maintainability
- Testability
- Security
- Production readiness
