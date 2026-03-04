# 🔐 Shield Vault API - Free Tier Roadmap (Batch 2026)

Welcome to the Shield Vault Engineering Lab. You are building an enterprise-grade Zero-Trust vault. High code standards and security awareness are mandatory.

## 📜 The Rules of the Vault

1. **Clean Architecture:** Keep the `domain` layer pure. Infrastructure details (DB/Auth) stay in `infrastructure`.
2. **Security-First:** Never log sensitive data (Passwords, Keys, JWTs).
3. **The 80% Rule:** No PR will be merged without 80% test coverage and a passing `Ruff` lint check.

---

## 📅 Weekly Milestones

### Week 1: [issue-01] Domain Modeling

- **Objective:** Define the core data structures.
- **Task:** Create `User` and `FileMetadata` entities and Pydantic schemas.
- **Constraint:** Do not use SQLAlchemy types in your Pydantic schemas. Keep them decoupled.

### Week 2: [issue-03] Encryption Utility

- **Objective:** Build the core security engine.
- **Task:** Implement AES-256 encryption/decryption utilities using the `cryptography` library.
- **Constraint:** Use GCM (Galois/Counter Mode) for authenticated encryption.

### Week 3: [issue-05] Repository & Metadata CRUD

- **Objective:** Manage secure metadata.
- **Task:** Implement the File Repository and the `GET /files` endpoint.
- **Constraint:** Ensure the query filters data based on the `current_user` ID.

### Week 4: [issue-07] The Hardening Sprint

- **Objective:** Prove the vault is secure.
- **Task:** Write comprehensive test suites using `pytest` and `pytest-asyncio`.
- **Constraint:** You must test both Success and Failure (Unauthorized) states for all endpoints.

---

## 🚀 Ready to Start?

1. Fork the repo.
2. Spin up the stack: `docker-compose -f docker-compose.dev.yml up`
3. Open a PR with the title: `feat(free-tier): Week 1 - [Your Name]`

_Stuck on encryption logic? Want a Senior Backend Engineer to review your architecture? Upgrade to **FastTrack Accelerator (₹399)**._
