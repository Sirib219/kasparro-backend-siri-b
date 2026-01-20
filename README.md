🚀 Kasparro Backend & ETL System
A production-ready Backend + ETL system that ingests crypto asset data from multiple sources, normalizes it into a unified schema, stores it in PostgreSQL, and exposes it via a REST API.


🔗 Live Deployment (Render)
Backend API (Live):
👉 https://kasparro-backend-siri-b-2.onrender.com
Swagger API Docs:
👉 https://kasparro-backend-siri-b-2.onrender.com/docs
Health Check:
👉 https://kasparro-backend-siri-b-2.onrender.com/health

📌 Features
✅ Multi-source ETL pipeline
CoinGecko API
CoinPaprika API
CSV file ingestion
✅ Canonical normalized schema
✅ PostgreSQL persistence
✅ Automatic ETL on container startup
✅ Schema drift detection
✅ REST API with pagination & filtering
✅ Dockerized & cloud deployed (Render)
✅ No hardcoded secrets (env-based config)

🏗️ Architecture Overview
Sources (APIs / CSV)
        ↓
   Raw Data Tables
        ↓
 Normalization Layer
        ↓
NormalizedAsset Table
        ↓
   FastAPI REST API

🧪 API Endpoints
🔍 Get Normalized Data
GET /data
Query Paramete
Name	Type	Default	Description
limit	int	10	Number of records (max 100)
offset	int	0	Pagination offset
source	str	null	Filter by source

Example
/data?limit=5&offset=0

❤️ Health Check
GET /health
Response
{
  "database": "connected",
  "etl_last_run_status": "success",
  "etl_last_run_at": "2026-01-20T08:25:25.879493"
}

📊 ETL Status
GET /stats
Response
{
  "sources": [
    { "source": "coingecko", "status": "success" },
    { "source": "coinpaprika", "status": "success" },
    { "source": "csv", "status": "success" }
  ]
}

🐳 Run Locally (Docker)
1️⃣ Clone Repository
git clone https://github.com/Sirib219/kasparro-backend-siri-b.git
cd kasparro-backend-siri-b

2️⃣ Create .env file
DATABASE_URL=postgresql://postgres:postgres@db:5432/crypto
.env is ignored by Git (.gitignore)

3️⃣ Build & Run
docker compose down -v
docker compose build
docker compose up

4️⃣ Access Locally
API: http://localhost:8000
Swagger: http://localhost:8000/docs
Health: http://localhost:8000/health

🧠 ETL Behavior
ETL runs automatically on container startup
Raw data stored per source
Normalized records stored in a unified schema
ETL checkpoints tracked per source
Schema drift logged for transparency

🔐 Security
❌ No secrets committed
✅ Environment variables via .env
✅ .env.example provided
✅ Production secrets managed in Render Environment Variables

🧰 Tech Stack
Backend: FastAPI
Database: PostgreSQL
ORM: SQLAlchemy
ETL: Python
Containerization: Docker & Docker Compose
Deployment: Render

📂 Project Structure
.
├── api/              # FastAPI routes
├── core/             # DB config & models
├── ingestion/        # ETL logic
├── services/         # Normalization services
├── data/             # CSV data
├── schemas/          # Pydantic schemas
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
├── .env.example
└── README.md

✅ Assignment Status
✔ Dockerized backend
✔ Multi-source ETL
✔ Normalization implemented
✔ No hardcoded secrets
✔ Public cloud deployment
✔ Verifiable live URL

👤 Author
Siri B
GitHub: https://github.com/Sirib219
