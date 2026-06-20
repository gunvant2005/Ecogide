# Deployment Guide - EcoGuide on Vercel

## Prerequisites

- GitHub account
- Vercel account
- Git installed locally

## Step 1: Push to GitHub

### Create a new GitHub repository

1. Go to [GitHub.com](https://github.com)
2. Click the **+** icon in the top right and select **New repository**
3. Name it `ecoguide` (or your preferred name)
4. Do NOT initialize with README (we already have one)
5. Copy the repository URL

### Push your code

```bash
cd c:\Users\dhake\OneDrive\Apps\Desktop\prototype
git remote add origin https://github.com/YOUR_USERNAME/ecoguide.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username and use the URL from your repository.

## Step 2: Deploy to Vercel

### Option A: Via Vercel Dashboard

1. Go to [Vercel.com](https://vercel.com)
2. Sign in with your GitHub account
3. Click **Add New...** → **Project**
4. Select your `ecoguide` repository
5. Vercel will auto-detect the configuration from `vercel.json`
6. Click **Deploy**

### Option B: Via Vercel CLI

```bash
npm i -g vercel
vercel --prod
```

## Environment Variables

On Vercel Dashboard, set these environment variables in your project settings:

```
FLASK_ENV=production
PYTHONUNBUFFERED=1
VITE_API_URL=https://your-vercel-domain.vercel.app
```

## Testing Before Deployment

### Backend Tests
```bash
cd backend
python -m pytest tests/ -v
```

All 13 tests should pass ✓

### Frontend Build
```bash
cd frontend
npm run build
```

## Project Structure

```
├── api/                    # Vercel serverless functions
│   └── index.py           # Flask app handler for Vercel
├── backend/               # Flask API
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── constants.py
│   │   └── services/
│   ├── tests/             # 13 automated tests
│   ├── requirements.txt
│   └── pytest.ini
├── frontend/              # React + TypeScript UI
│   ├── src/
│   ├── package.json
│   └── vite.config.ts
├── vercel.json            # Deployment configuration
└── .env.example           # Environment variables template
```

## Key Features Deployed

- ✅ **Dashboard** - View carbon footprint summary
- ✅ **Activity Logging** - Log transport, food, energy, shopping
- ✅ **Insights** - Personalized recommendations
- ✅ **Assistant Chat** - AI-powered carbon guidance
- ✅ **Profile Management** - Customize calculations
- ✅ **Simulator** - Explore impact of changes

## Testing Summary

All tests pass:
- API endpoints (health, profile CRUD, activities)
- Carbon emission calculations
- Footprint summarization
- Insights and recommendations
- Assistant intent detection

## Troubleshooting

### API Connection Issues
- Check `VITE_API_URL` environment variable matches your Vercel domain
- Ensure CORS is configured in `backend/app/main.py`

### Build Failures
- Verify `requirements.txt` has all Python dependencies
- Check `frontend/package.json` includes all npm packages
- Review Vercel build logs in the dashboard

### Database Issues
- Data persists in Vercel's `/tmp` storage (temporary)
- For production, integrate with a database service (MongoDB, PostgreSQL)

## Next Steps

1. Push code to GitHub
2. Connect GitHub repository to Vercel
3. Deploy and test
4. Share your live URL!

---

**Deployed URL**: `https://[your-project].vercel.app`
