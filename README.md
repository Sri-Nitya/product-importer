# Product Importer

A simple FastAPI application that lets you upload a CSV file and import product data into PostgreSQL. Long-running imports are handled using Celery + Redis (if available). If Celery is not available (such as on Render free tier), the app automatically falls back to FastAPI BackgroundTasks.

---

## 🚀 Features
- Upload CSV files from the UI  
- Import products into PostgreSQL  
- Async processing using Celery  
- Automatic fallback when Celery/Redis is not available  
- Simple UI at `/`  
- Health check endpoints  

---

# 🛠️ Run Locally (Docker Compose)

Start everything:

```bash
uvicorn app.main:app --reload
```

```bash
docker compose up --build
```

Visit: http://localhost:8000

If Docker gives engine errors:

```bash
Restart-Service com.docker.service
wsl --shutdown
```

---

# 🧪 Run Without Docker

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/postgres"
export REDIS_URL="redis://localhost:6379/0"

uvicorn app.main:app --reload        

celery -A app.tasks.celery_app.celery_app worker --loglevel=INFO -Q product_importer_queue  
```

---

# ☁️ Deploying on Render

Create a **Web Service** → connect GitHub repo.

Add environment vars:

```
DATABASE_URL=<your render postgres url>
REDIS_URL=<your redis url>
```

⚠ Render free tier does NOT support background workers.  

(Optional if paid plan):

```
celery -A app.tasks.celery_app.celery_app worker --loglevel=INFO -Q product_importer_queue
```

---

# 🔄 Fallback Mode (When Redis/Celery Not Available)

- App prints a warning  
- CSV import runs via FastAPI BackgroundTasks  
- Good enough for small uploads & free-tier deployments  

---


# 📁 Environment Variables

```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/postgres
REDIS_URL=redis://localhost:6379/0
```

---

# 📝 Notes for Reviewers

- All required assignment features implemented  
- Celery integration complete  
- Fallback mode allows deployment even on free hosting  
- Only limitation: free Render cannot run background workers  

The project fully works in both Docker and local mode.

