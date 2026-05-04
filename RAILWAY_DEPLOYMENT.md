# Railway Deployment Guide

## Prerequisites
1. Railway account (sign up at https://railway.app)
2. (Optional) GitHub account if you want auto-deploy from repo
3. Railway CLI for direct deploy from local Docker context

Install Railway CLI:

```bash
npm i -g @railway/cli
railway login
```

## Direct Docker Deployment (No GitHub Required)

From your backend folder, deploy directly with Dockerfile:

```bash
cd /home/anurag/Projects/LibraryManagement/library-management/backend
railway init
railway up
```

Railway detects the Dockerfile and builds/deploys it directly.

## Alternative: GitHub Auto-Deploy

If you prefer auto-deploy on each push, use GitHub integration.

## Step 1: Push Code to GitHub

```bash
cd /home/anurag/Projects/LibraryManagement/library-management
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/library-management.git
git branch -M main
git push -u origin main
```

## Step 2: Create Railway Project

1. Go to https://railway.app/dashboard
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Authorize Railway with your GitHub account
5. Select your `library-management` repository
6. Choose the branch (main)

For Dockerfile projects, set root directory to `backend` so Railway builds with `backend/Dockerfile`.

## Step 3: Configure Backend Service

### Create MySQL Database
1. In Railway dashboard, click "Add Service"
2. Choose "MySQL"
3. Click "Deploy"
4. Note the credentials (they'll be in the service variables)

### Create Redis Cache
1. Click "Add Service"
2. Choose "Redis"
3. Click "Deploy"

### Deploy Backend
1. Click "Add Service"
2. Choose "GitHub Repo"
3. Select your repository
4. Set Root Directory: `backend`
5. Click "Deploy"

If using direct deploy (`railway up`), this service is created automatically.

## Step 4: Configure Environment Variables

Go to your backend service → Variables tab, add:

```
DATABASE_URI=mysql+pymysql://USER:PASSWORD@HOST:PORT/DATABASE
REDIS_URL=redis://USER:PASSWORD@HOST:PORT/0
SECRET_KEY=your-very-secret-key-change-this
DEBUG=False
```

**How to get these values:**
- For DATABASE_URI: Check MySQL service variables in Railway dashboard
  Format: `mysql+pymysql://username:password@host:port/database`
  
- For REDIS_URL: Check Redis service variables in Railway dashboard
  Format: `redis://default:password@host:port/0`

## Step 5: Generate Public URL

1. Go to your backend service
2. Look for "Public URL" or "Domain" section
3. Click "Generate Domain" if not already set
4. You'll get a URL like: `https://library-backend-prod.railway.app`

## Step 6: Run Database Migrations

After deployment, you need to run Alembic migrations:

1. Go to your backend service → Deployments tab
2. Click the latest deployment
3. Open the command terminal/console
4. Run: `alembic upgrade head`

Or add to Dockerfile (recommended):
```dockerfile
# After the CMD line in Dockerfile, modify to:
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
```

Note: Railway provides the `PORT` environment variable automatically. The Dockerfile is already configured to use it.

## Step 7: Update CORS in Backend

Update [backend/app/main.py](../app/main.py#L8-L14) CORS configuration:

```python
allow_origins=[
    "http://localhost:3000",
    "http://localhost",
    "capacitor://localhost",
    "https://your-app-domain.railway.app",  # Add Railway domain
    "https://*.railway.app",  # Allow all Railway domains
]
```

Commit and push to GitHub - Railway will auto-redeploy.

## Troubleshooting

### Service won't start
- Check logs: Click deployment → View logs
- Verify environment variables are set correctly
- Ensure database migrations ran successfully

### Database connection error
- Verify DATABASE_URI format
- Check if MySQL service is running
- Ensure MySQL service and backend service are connected

### Timeout errors
- Check application logs for errors
- Verify health check endpoint exists (/docs)
- May need to increase Railway's memory/cpu allocation

## After Railway Deployment - Android App Changes

See the next section in this guide for required Android app updates.
