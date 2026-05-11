# Nexus: Enterprise Internal Operations Portal

Nexus is a full-stack internal operations platform designed to streamline employee engagement, feedback management, and real-time operational tracking. The system features an automated **Decision Support Engine** for handling employee complaints and a data-driven dashboard for administrative insights.

## 🏗 Architecture & Engineering Decisions

### System Architecture
```mermaid
graph TD
    User((Employee / Admin))
    
    subgraph "Frontend Layer (React + Vite)"
        UI[Web Dashboard]
        State[State Management / Axios]
    end
    
    subgraph "Backend Layer (FastAPI)"
        API[REST API Endpoints]
        Service[InternalPortalService]
        Engine[Decision Support Engine]
    end
    
    subgraph "Data Layer (PostgreSQL)"
        DB[(Postgres DB)]
        Schema[Schema: internal_portal]
    end

    User <--> UI
    UI <--> State
    State <--> API
    API <--> Service
    Service <--> Engine
    Service <--> Schema
    Schema <--> DB
```

## 📊 Data Pipeline & Lifecycle

The system implements a streamlined data pipeline following the **Medallion Architecture** principles to ensure data quality and traceability:

```mermaid
graph LR
    A[Raw Input] -->|Ingestion| B(Bronze: Raw Tables)
    B -->|Validation| C(Silver: Structured Data)
    C -->|Decision Support Engine| D(Gold: Analysis & Insights)
    D -->|Reporting| E[Management Dashboard]
    
    style B fill:#cd7f32,stroke:#333
    style C fill:#c0c0c0,stroke:#333
    style D fill:#ffd700,stroke:#333
```

- **Bronze (Ingestion)**: Captures raw employee feedback and operational data in their original form.
- **Silver (Processing)**: Sanitizes and structures data using SQLAlchemy models, ensuring schema integrity and handling background synchronization.
- **Gold (Insights)**: The **Decision Support Engine** enriches the data with automated department routing, priority scoring, and recommended actions, transforming raw records into actionable insights.

### 1. Database & Schema Strategy
- **Multi-Schema Design**: Implements logical separation within PostgreSQL using custom schemas (`internal_portal`). This ensures a clear boundary between core operational data and potential future integrations.
- **Medallion-inspired Processing**: Although a single-node setup, the data flows from raw submission (Bronze) to analyzed results (Gold) within the `Complaint` lifecycle, ensuring auditability of automated recommendations.

### 2. Backend Implementation (FastAPI)
- **Asynchronous Execution**: Leverages Python's `asyncio` and FastAPI's background tasks for non-blocking ETL processes and data seeding.
- **Robust Initialization**: Features a custom database initialization wrapper with retry logic to ensure stability in containerized environments (handling race conditions during DB startup).
- **Extensible Service Layer**: Business logic is decoupled into a dedicated `InternalPortalService`, following the Service Layer Pattern for better maintainability and testing.

### 3. Frontend & UX (React + Vite)
- **Modern Component Architecture**: Built with React and Vite for optimal build performance.
- **State Management**: Implements efficient data fetching and polling mechanisms to keep administrative dashboards updated in real-time.

## 🚀 Getting Started

### Prerequisites
- Docker & Docker Compose
- (Optional) Python 3.9+ & Node.js 18+ for local development

### Deployment via Docker (Recommended)
The easiest way to spin up the entire ecosystem (App + PostgreSQL) is using Docker Compose:

```bash
docker-compose up --build
```

Access the application at: `http://localhost:5173`

### Manual Setup

#### Backend
1. Create a virtual environment: `python -m venv venv`
2. Install dependencies: `pip install -r backend/requirements.txt`
3. Configure `.env` variables
4. Start the server: `cd backend && uvicorn app.main:app --reload`

#### Frontend
1. Install dependencies: `cd frontend && npm install`
2. Start development server: `npm run dev`

## 🛠 Tech Stack
- **Backend**: FastAPI (Python), SQLAlchemy ORM
- **Frontend**: React.js, Vite, Vanilla CSS (Custom Design System)
- **Database**: PostgreSQL 15
- **Infrastructure**: Docker, Docker Compose
