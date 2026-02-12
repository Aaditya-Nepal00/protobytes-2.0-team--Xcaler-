#!/bin/bash

# Project Sachet - Production Deployment Script

echo "🚀 Deploying Project Sachet to production..."

# Build and push Docker images
echo "🐳 Building Docker images..."
docker-compose -f docker-compose.prod.yml build

# Push to registry (if using)
# docker-compose -f docker-compose.prod.yml push

# Deploy services
echo "📡 Starting services..."
docker-compose -f docker-compose.prod.yml up -d

# Run migrations
echo "🗄️  Running database migrations..."
docker-compose -f docker-compose.prod.yml exec backend flask db upgrade

echo "✅ Deployment complete!"
echo "🌐 Application is now live"
echo "📊 Check status: docker-compose ps"
echo "📋 View logs: docker-compose logs -f"
