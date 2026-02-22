# 🤝 Contributing to Shield Vault API

Welcome to the Blyno Backend Engineering workflow.

This project follows enterprise-grade development discipline.

---

## 🔀 Branch Naming Convention

All branches must follow:

```

feature/<name>
bugfix/<name>
hotfix/<name>
chore/<name>
docs/<name>

Example:

feature/file-encryption

```

Invalid branch names will fail CI.

---

## 🛠 Development Workflow

1. Create feature branch
2. Implement changes
3. Write tests
4. Ensure coverage ≥ 85%
5. Run local Docker environment
6. Open Pull Request
7. Await approval

Direct pushes to `main` are prohibited.

---

## 🧪 Testing Requirements

All PRs must:

- Pass linting (Ruff)
- Pass type checking (Mypy)
- Pass Bandit security scan
- Pass CodeQL analysis
- Maintain ≥ 85% test coverage

Run locally:

```bash
pytest --cov=app
```

---

## 🛡 Security Guidelines

- Never commit `.env`
- Never hardcode secrets
- Always validate user input
- Avoid storing plaintext sensitive data
- Review encryption-related logic carefully

---

## 📂 Clean Architecture Rules

- Domain must not depend on FastAPI
- Infrastructure must not leak into Domain
- Application layer contains business logic
- API layer only handles HTTP concerns

Violations will be rejected in review.

---

## 🏢 Code Review Standards

Reviewers will check:

- Architectural correctness
- Security implications
- Edge cases
- Logging consistency
- Error handling quality

---

## 🚨 Zero-Tolerance Rules

PR will be rejected if:

- Security checks fail
- Coverage drops below threshold
- Branch name invalid
- Migration missing for schema changes

---

Thank you for maintaining engineering discipline.

