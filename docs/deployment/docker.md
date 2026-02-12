# Docker Deployment Guide

## Docker Files

### backend/Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["flask", "run", "--host=0.0.0.0"]
```

### frontend/Dockerfile

```dockerfile
FROM node:16-alpine as builder

WORKDIR /app
COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## Docker Compose

### docker-compose.yml (Development)

```yaml
version: '3.8'

services:
  db:
    image: postgres:13
    environment:
      POSTGRES_USER: sachet
      POSTGRES_PASSWORD: dev_password
      POSTGRES_DB: sachet_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build: ./backend
    environment:
      DATABASE_URL: postgresql://sachet:dev_password@db:5432/sachet_db
      FLASK_ENV: development
    ports:
      - "5000:5000"
    depends_on:
      - db
    volumes:
      - ./backend:/app

  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
    volumes:
      - ./frontend:/app
      - /app/node_modules

volumes:
  postgres_data:
```

### docker-compose.prod.yml (Production)

```yaml
version: '3.8'

services:
  db:
    image: postgres:13
    environment:
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: ${DB_NAME}
    volumes:
      - postgres_prod_data:/var/lib/postgresql/data
    restart: always

  backend:
    build: ./backend
    environment:
      DATABASE_URL: postgresql://${DB_USER}:${DB_PASSWORD}@db:5432/${DB_NAME}
      FLASK_ENV: production
    depends_on:
      - db
    restart: always

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    restart: always

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - backend
      - frontend
    restart: always

volumes:
  postgres_prod_data:
```

## Building and Running

### Development

```bash
# Build all services
docker-compose build

# Start all services
docker-compose up

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Production

```bash
# Build with production Compose file
docker-compose -f docker-compose.prod.yml build

# Start services
docker-compose -f docker-compose.prod.yml up -d

# View specific service logs
docker-compose -f docker-compose.prod.yml logs backend
```

## Useful Commands

```bash
# Execute command in container
docker-compose exec backend flask db upgrade

# Bash shell in container
docker-compose exec backend bash

# Restart service
docker-compose restart backend

# Remove containers and volumes
docker-compose down -v

# List running containers
docker-compose ps
```

## Optimization Tips

1. Use multi-stage builds for frontend
2. Keep image sizes small with Alpine
3. Use `.dockerignore` files
4. Implement health checks
5. Use persistent volumes for data

## Security Best Practices

1. Use specific image versions (not `latest`)
2. Run containers as non-root user
3. Limit container resources
4. Scan images for vulnerabilities
5. Keep secrets in environment variables

---

See [Production Deployment](production.md) for full deployment guide.
