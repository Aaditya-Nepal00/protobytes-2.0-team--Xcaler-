# Production Deployment Guide

## Prerequisites

- Docker and Docker Compose
- PostgreSQL 12+
- Redis (for caching)
- Nginx/Reverse Proxy
- SSL Certificate

## Deployment Steps

### 1. Environment Configuration

Create production `.env` files:

**backend/.env**
```env
FLASK_ENV=production
FLASK_APP=run.py
SECRET_KEY=<generate-strong-secret>
DATABASE_URL=postgresql://user:strong_password@postgres-host/sachet_db
JWT_SECRET_KEY=<generate-strong-secret>
```

**frontend/.env**
```env
VITE_API_BASE_URL=https://api.yourdomain.com/api
VITE_APP_NAME=Project Sachet
VITE_APP_VERSION=0.1.0
```

### 2. Database Migration

```bash
# Connect to production database
flask db upgrade
```

### 3. Build and Deploy with Docker

```bash
# Build images
docker-compose -f docker-compose.prod.yml build

# Start services
docker-compose -f docker-compose.prod.yml up -d
```

### 4. SSL/TLS Configuration

Use Let's Encrypt with Certbot:
```bash
certbot certonly --standalone -d yourdomain.com
```

Update Nginx configuration with SSL certificate paths.

### 5. Nginx Configuration

```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    location /api/ {
        proxy_pass http://backend:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location / {
        proxy_pass http://frontend:3000;
        proxy_set_header Host $host;
    }
}

server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}
```

### 6. Backup Strategy

Schedule regular database backups:
```bash
# Daily backup
0 2 * * * pg_dump database_name > backup_$(date +\%Y\%m\%d).sql
```

## Monitoring

### Health Checks

Setup health check endpoints:
- `/health` - Application health
- `/api/health` - API health

### Logging

Configure centralized logging:
- Use ELK Stack or similar
- Monitor error rates
- Track performance metrics

### Alerts

Set up alerts for:
- Service downtime
- High error rates
- Database issues
- Disk space

## Performance Optimization

1. Enable Redis caching
2. Optimize database queries
3. Use CDN for static files
4. Enable GZIP compression
5. Implement rate limiting

## Security Checklist

- [ ] HTTPS enabled
- [ ] CORS properly configured
- [ ] Input validation enabled
- [ ] SQL injection prevention
- [ ] XSS protection enabled
- [ ] CSRF tokens implemented
- [ ] Secrets not in code
- [ ] Regular security updates

## Maintenance

### Regular Tasks

1. Update dependencies monthly
2. Monitor and analyze logs
3. Review security patches
4. Test backup restoration
5. Performance audits

### Scaling

For handling increased load:
- Horizontal scaling with load balancer
- Database read replicas
- Caching layer expansion
- CDN distribution

---

See [Docker Configuration](docker.md) for containerization details.
