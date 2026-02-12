# Environment Setup

## Configuration Files

### Frontend `.env`
Location: `frontend/.env`

```env
VITE_API_BASE_URL=http://localhost:5000/api
VITE_APP_NAME=Project Sachet
VITE_APP_VERSION=0.1.0
```

### Backend `.env`
Location: `backend/.env`

```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@localhost:5432/sachet_db
JWT_SECRET_KEY=your-jwt-secret-key
```

## Environment Variables

### Frontend Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `VITE_API_BASE_URL` | Backend API URL | `http://localhost:5000/api` |
| `VITE_APP_NAME` | Application name | `Project Sachet` |
| `VITE_APP_VERSION` | App version | `0.1.0` |

### Backend Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `FLASK_ENV` | Environment | `development` |
| `FLASK_APP` | Entry point | `run.py` |
| `SECRET_KEY` | Secret key for sessions | Generate with `os.urandom(24)` |
| `DATABASE_URL` | PostgreSQL connection | `postgresql://user:pass@localhost/db` |
| `JWT_SECRET_KEY` | JWT signing key | Generate a strong secret |

## Database URL Format

```
postgresql://[user[:password]]@[host][:port]/[database]
```

Examples:
```
postgresql://postgres:password@localhost:5432/sachet_db
postgresql://user@localhost/sachet_db
```

## Generating Secrets

### Python
```python
import os
print(os.urandom(24).hex())
```

### Command Line
```bash
# macOS/Linux
openssl rand -hex 12

# Windows PowerShell
[Convert]::ToHexString([System.Security.Cryptography.RandomNumberGenerator]::GetBytes(12))
```

## Production Configuration

For production deployment:
1. Use strong, unique secrets
2. Use environment-specific values
3. Store secrets securely (not in git)
4. Use a secrets manager (AWS Secrets Manager, HashiCorp Vault, etc.)
5. Enable HTTPS/SSL
6. Set `FLASK_ENV=production`

---

See [Local Development](local_development.md) for full setup instructions.
