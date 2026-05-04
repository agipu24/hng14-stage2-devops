# FIXES.md

## Fix 1
- **File:** api/main.py
- **Line:** 6
- **Problem:** Redis host hardcoded as `localhost` — fails inside Docker containers
- **Fix:** Changed to `os.getenv("REDIS_HOST", "redis")`

## Fix 2
- **File:** worker/worker.py
- **Line:** 5
- **Problem:** Redis host hardcoded as `localhost` — fails inside Docker containers
- **Fix:** Changed to `os.getenv("REDIS_HOST", "redis")`

## Fix 3
- **File:** api/main.py
- **Problem:** Missing `/health` endpoint — required for Docker healthcheck
- **Fix:** Added `GET /health` endpoint returning `{"message": "healthy"}`

## Fix 4
- **File:** worker/worker.py
- **Problem:** No error handling — if Redis is unavailable, worker crashes permanently
- **Fix:** Wrapped main loop in try/except with 3 second retry delay

## Fix 5
- **File:** frontend/app.js
- **Line:** 6
- **Problem:** API_URL hardcoded as `http://localhost:8000` — fails in Docker
- **Fix:** Changed to `process.env.API_URL || "http://api:8000"`

## Fix 7
- **File:** frontend/
- **Problem:** Missing package-lock.json — `npm ci` requires it and fails without it
- **Fix:** Generated package-lock.json by running `npm install`, changed Dockerfile to use `npm install --omit=dev`
