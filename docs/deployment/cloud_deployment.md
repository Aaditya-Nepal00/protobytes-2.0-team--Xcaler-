# Hackathon Deployment Guide - Vercel & Railway

Simple, quick deployment for prototyping using Vercel (frontend) and Railway (backend).

## Frontend Deployment - Vercel

### Prerequisites
- GitHub account with repository pushed
- Vercel account (free tier)

### Step 1: Connect GitHub to Vercel

1. Go to [vercel.com](https://vercel.com)
2. Sign up with GitHub
3. Click "Import Project"
4. Select your repository

### Step 2: Configure Frontend

1. **Root Directory:** `frontend`
2. **Build Command:** `npm run build`
3. **Output Directory:** `dist`
4. **Environment Variables:**
   ```
   VITE_API_BASE_URL=https://your-railway-backend.up.railway.app/api
   ```

### Step 3: Deploy

1. Click "Deploy"
2. Wait for build to complete (2-3 minutes)
3. Get your live URL: `https://your-app.vercel.app`

✅ **That's it! Frontend is live and auto-deploys on every GitHub push**

---

## Backend Deployment - Railway

### Prerequisites
- GitHub account with repository
- Railway account (free tier at [railway.app](https://railway.app))
- PostgreSQL database

### Step 1: Create Railway Project

1. Go to [Railway Dashboard](https://railway.app)
2. Click "New Project"
3. Select "GitHub Repo"
4. Connect your GitHub repository

### Step 2: Add PostgreSQL Database

1. In Project, click "+ Create"
2. Select "Database"
3. Choose "PostgreSQL"
4. Railway creates the database automatically

### Step 3: Deploy Backend

#### Backend Configuration File - `backend/Procfile`
```
web: gunicorn app:app
```

#### Update `backend/requirements.txt` - Add:
```
gunicorn==20.1.0
python-dotenv==0.21.0
```

#### Update `backend/run.py`
```python
from app import create_app
import os

app = create_app(os.getenv('FLASK_ENV', 'production'))

if __name__ == '__main__':
    app.run(debug=False)
```

### Step 4: Set Environment Variables in Railway

In Railway Dashboard → Variables:

```
FLASK_ENV=production
SECRET_KEY=generate-random-string
JWT_SECRET_KEY=generate-random-string
DATABASE_URL=<auto-populated from PostgreSQL>
```

### Step 5: Deploy

1. Railway auto-detects Python project
2. Runs `pip install -r requirements.txt`
3. Executes Procfile command
4. Backend live in 2-3 minutes
5. Get URL: `https://your-railway-backend.up.railway.app`

✅ **Backend is deployed! Auto-deploys on GitHub push**

---

## Database Setup on Railway

Railway creates PostgreSQL automatically, but you need to run migrations:

### Option 1: Railway CLI

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Run migrations in Railway environment
railway run flask db upgrade
```

### Option 2: One-time Setup

Add to `backend/run.py` initialization:
```python
from app import db, create_app

with app.app_context():
    db.create_all()  # Creates tables on startup
```

---

## Connect Frontend to Backend

Update `frontend/.env` in Vercel:

```
VITE_API_BASE_URL=https://your-backend.up.railway.app/api
```

Then redeploy frontend (or it auto-redeploys on push).

---

## Quick Troubleshooting

### Frontend Won't Deploy
- Check `frontend/` folder exists
- Verify `npm run build` works locally
- Check build logs in Vercel dashboard

### Backend Won't Deploy
- Ensure `Procfile` exists in `backend/`
- Check `requirements.txt` has `gunicorn`
- View logs in Railway dashboard

### API Connection Failed
- Verify `VITE_API_BASE_URL` matches Railway URL
- Check CORS enabled in Flask
- Test API manually: `curl https://backend-url/api/health`

---

## Cost

✅ **Completely Free for Hackathon:**
- Vercel: Free tier (unlimited deployments)
- Railway: Free tier ($5/month credit, more than enough)
- PostgreSQL: Free on Railway

---

## Auto-Deploy on Every Push

Both platforms auto-deploy when you push to GitHub:

```bash
git add .
git commit -m "Update features"
git push origin main
```

Changes live in 2-3 minutes! Perfect for hackathon rapid iteration.

---

## See Also

- [Local Development Guide](../setup/local_development.md)
- [Environment Setup](../setup/environment_setup.md)
