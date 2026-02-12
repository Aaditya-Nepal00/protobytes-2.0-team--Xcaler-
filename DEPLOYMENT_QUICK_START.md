# Hackathon Deployment Checklist

Quick deployment checklist for Vercel (Frontend) + Railway (Backend)

## Pre-Deployment (5 minutes)

- [ ] Push code to GitHub
- [ ] Test locally: `npm run dev` + `flask run`
- [ ] Verify `.env.example` files exist in both frontend and backend

## Frontend - Vercel (5 minutes)

- [ ] Visit [vercel.com](https://vercel.com)
- [ ] Sign in with GitHub
- [ ] Click "Import Project"
- [ ] Select your repository
- [ ] Set Root Directory: `frontend`
- [ ] Build Command: `npm run build`
- [ ] Output Directory: `dist`
- [ ] Add Environment Variable:
  - `VITE_API_BASE_URL` = (your Railway backend URL)/api
- [ ] Click Deploy
- [ ] Wait 2-3 minutes
- [ ] Note your frontend URL: `https://xxx.vercel.app`

## Backend - Railway (10 minutes)

### Database Setup
- [ ] Visit [railway.app](https://railway.app)
- [ ] Sign in with GitHub
- [ ] Create New Project
- [ ] Add PostgreSQL
- [ ] Note the DATABASE_URL (auto-created)

### Backend Deployment
- [ ] In Railway, add new service from GitHub repo
- [ ] Select your repository
- [ ] Environment Variables:
  - `FLASK_ENV` = `production`
  - `SECRET_KEY` = (generate random string)
  - `JWT_SECRET_KEY` = (generate random string)
  - `DATABASE_URL` = (Railway auto-populates)
- [ ] Deploy
- [ ] Wait 2-3 minutes for build
- [ ] Note your backend URL: `https://xxx.up.railway.app`

### Database Migration (optional, for tables)
```bash
railway run flask db upgrade
```

Or add to `backend/run.py`:
```python
with app.app_context():
    db.create_all()
```

## Post-Deployment

- [ ] Update `frontend/.env.example` with live backend URL
- [ ] Test API connection
- [ ] Share live URL with team! 🎉

## Testing Live Deployment

**Frontend is running at:**
```
https://xxx.vercel.app
```

**Backend API is running at:**
```
https://xxx.up.railway.app/api
```

**Test API health:**
```bash
curl https://xxx.up.railway.app/api/health
```

## Auto-Deploy

Both Vercel and Railway auto-deploy on GitHub push:

```bash
git add .
git commit -m "Update features"
git push origin main
```

Connected and live in 2-3 minutes! Perfect for rapid iteration during hackathon.

## Troubleshooting

**"Cannot connect to API"**
- Check backend URL matches VITE_API_BASE_URL
- Verify CORS enabled in Flask
- Check Railway backend is running (green in dashboard)

**"Build failed on Vercel"**
- View build logs in Vercel dashboard
- Ensure `frontend/` folder exists
- Check `npm run build` works locally

**"Build failed on Railway"**
- View logs in Railway dashboard
- Ensure Procfile exists in backend/
- Check requirements.txt has all dependencies

---

**Total time: ~20 minutes from start to live deployment!** 🚀
