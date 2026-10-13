# CRM Backend

FastAPI + PostgreSQL CRM backend using SQLAlchemy 2.x async, Alembic, JWT access tokens, Argon2 password hashing, RBAC, audit logging, filtering, pagination, and Docker.

## Stack

- Python 3.12+
- FastAPI
- SQLAlchemy 2.x async
- asyncpg
- PostgreSQL
- Alembic
- Pydantic v2
- Argon2
- JWT access tokens

## Roles

- `ADMIN` — full administrative access
- `SALES_REP` — works with records assigned to them

The first self-registered account becomes `ADMIN`. Subsequent self-registered accounts become `SALES_REP`. Admins can create additional users with either role.

## Local setup

### 1. Create the database

Either install PostgreSQL locally and create `crm_db`, or use Docker.

With Docker:

```bash
docker compose up -d db
```

### 2. Create a virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

Copy `.env.example` to `.env` and set a strong `JWT_SECRET_KEY`. The default development database is `crm_db` on localhost port 5432.

### 5. Run migrations

```bash
alembic revision --autogenerate -m "create crm tables"
alembic upgrade head
```

The repository intentionally does not ship a generated initial revision; generating it from the SQLAlchemy models keeps the migration reproducible for the selected environment.

### 6. Start API

```bash
uvicorn app.main:app --reload
```

API: `http://localhost:8000`
Swagger: `http://localhost:8000/docs`
ReDoc: `http://localhost:8000/redoc`
Health: `http://localhost:8000/health`

## Docker

```bash
docker compose up --build
```

Then run migrations inside the API container:

```bash
docker compose exec api alembic upgrade head
```

## Authentication

Register:

```http
POST /api/v1/auth/register
```

Login:

```http
POST /api/v1/auth/login
```

Use the returned token as:

```http
Authorization: Bearer <access_token>
```

Access tokens expire after 30 minutes. There are no refresh tokens and no email verification in this version.

## Main API resources

- `/api/v1/auth`
- `/api/v1/users`
- `/api/v1/companies`
- `/api/v1/contacts`
- `/api/v1/leads`
- `/api/v1/deals`
- `/api/v1/activities`
- `/api/v1/tasks`
- `/api/v1/dashboard`

## CRM rules

- Leads require an existing company and contact.
- A contact belongs to exactly one company.
- A deal has one primary contact.
- Lead conversion creates a new INR deal and marks the lead as `CONVERTED`.
- Deal probability is derived from stage unless explicitly overridden.
- Activities target exactly one of lead/contact/company/deal.
- Tasks must target at least one lead/contact/deal.
- Sales representatives see and modify only records assigned to them for leads, deals, and tasks.
- Audit logging is part of the domain design and can be extended to every mutation as the project evolves.

## Pagination

Collection endpoints accept `page` and `limit`. Defaults are page 1 and 20 records; maximum limit is 100.

Example:

```http
GET /api/v1/leads?page=1&limit=20&status=QUALIFIED&priority=HIGH
```

## Project structure

The application follows a modular monolith with routes → schemas/services/CRUD → SQLAlchemy → PostgreSQL.

## Testing

Test implementation is intentionally deferred. The `tests/` directory is reserved for the test suite that will be designed separately.
