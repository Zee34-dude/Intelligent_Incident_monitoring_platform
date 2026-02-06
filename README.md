# 🚀 AIOps Incident Monitoring Platform

An intelligent incident management and monitoring platform built with FastAPI. Monitor your services, automatically detect downtime, and track incidents with real-time metrics.

## ✨ Features

- **🔐 User Authentication** - JWT-based auth with email verification
- **🏢 Multi-tenant Organizations** - Business email required, role-based access
- **📡 Service Monitoring** - Automated health checks every 60 seconds
- **🚨 Incident Management** - Auto-create incidents on downtime, auto-resolve on recovery
- **📊 Analytics & Metrics** - Uptime %, MTTR, severity distribution, downtime tracking

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        FastAPI App                          │
├─────────────────────────────────────────────────────────────┤
│  Routers           │  Background Task                       │
│  • /user           │  • health_check_loop()                 │
│  • /login          │    └─ Runs every 60s                   │
│  • /verify-email   │    └─ Checks all services              │
│  • /organization   │    └─ Creates/resolves incidents       │
│  • /services       │                                        │
├─────────────────────────────────────────────────────────────┤
│            SQLAlchemy ORM + PostgreSQL (Supabase)           │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
app/
├── main.py              # FastAPI app entry point
├── database.py          # Database connection & session
├── models.py            # SQLAlchemy models
├── schemas.py           # Pydantic schemas
├── hasing.py            # Password hashing utilities
├── auth/
│   ├── token.py         # JWT token creation/verification
│   └── oaut2.py         # OAuth2 authentication
├── routers/
│   ├── user.py          # User CRUD endpoints
│   ├── authentication.py # Login & email verification
│   ├── organization.py  # Organization & service management
│   └── service.py       # Service metrics endpoints
├── controller/
│   ├── user_controller.py
│   ├── organization_controller.py
│   └── service_controller.py
└── health/
    ├── runner.py        # Background health check loop
    ├── checker.py       # HTTP health check logic
    └── utils.py         # Severity calculation utilities
```

## 🗄️ Data Models

| Model | Description |
|-------|-------------|
| **User** | Username, email, password, role (admin/user/viewer), verification status |
| **Organization** | Company/team that owns services, linked to users |
| **Service** | Website/endpoint to monitor (URL, status, response time) |
| **Incident** | Downtime event with severity (LOW/MEDIUM/HIGH/CRITICAL) and status (OPEN/INVESTIGATING/RESOLVED) |
| **EmailVerification** | Verification codes for email confirmation |

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- PostgreSQL database (or Supabase)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Intelligent_Incident_management_monitoring_platform
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # source .venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Create a `.env` file:
   ```env
   DATABASE_URL=postgresql://user:password@host:port/database
   SMTP_PASSWORD=your_smtp_app_password
   ```

5. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

6. **Start the server**
   ```bash
   uvicorn app.main:app --reload
   ```

7. **Access the API docs**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## 🔄 How Health Monitoring Works

1. **Background Loop** starts when the app launches
2. Every **60 seconds**, it checks all registered services
3. Makes an HTTP GET request to each service URL
4. If status code < 400 → **UP**, otherwise → **DOWN**
5. **Status Change Detection**:
   - UP → DOWN: Creates new incident with severity
   - DOWN → UP: Auto-resolves the incident
6. Updates service metadata (response time, last checked, error reason)

## 📊 Metrics Calculated

| Metric | Description |
|--------|-------------|
| **Uptime %** | Percentage of time service was operational |
| **MTTR** | Mean Time to Resolve (average incident duration) |
| **Total Downtime** | Cumulative downtime in seconds |
| **Current Downtime** | Ongoing downtime if service is DOWN |
| **Incident Count** | Total number of incidents |
| **Severity Distribution** | Count of incidents by severity level |

## 🔒 Authentication Flow

1. **Register** → `POST /user` (creates unverified user)
2. **Verify Email** → `POST /verify-email` (with 6-digit code)
3. **Login** → `POST /login` (returns JWT token)
4. **Use Token** → Add `Authorization: Bearer <token>` header

## 📝 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/user` | Create new user |
| GET | `/user/{id}` | Get user by ID |
| POST | `/login` | Authenticate and get JWT |
| POST | `/verify-email` | Verify email with code |
| POST | `/organization` | Create organization |
| POST | `/organization/{id}/service` | Add service to org |
| PATCH | `/organization/service/{id}` | Update service |
| GET | `/services/{org_id}/metrics` | Get service metrics |

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **ORM**: SQLAlchemy
- **Database**: PostgreSQL (Supabase)
- **Migrations**: Alembic
- **Auth**: JWT (python-jose)
- **HTTP Client**: httpx (async)
- **Password Hashing**: passlib

## 📄 License

MIT License
