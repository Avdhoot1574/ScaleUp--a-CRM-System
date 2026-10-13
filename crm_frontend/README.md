# Northstar CRM Frontend

Responsive React frontend for the existing FastAPI + PostgreSQL CRM backend. It uses the current backend contract under `/api/v1` and does not add passkey registration or admin-approval workflows.

## Features

- JWT login and public registration using the backend's JSON request schemas
- Session restoration via `GET /auth/me`; bearer token attached to API requests
- Dashboard using `GET /dashboard/summary` plus recent leads, deals, and tasks
- CRUD screens for companies, contacts, leads, deals, tasks, and users (users are admin-only)
- Activity listing and creation; the backend currently exposes activities as read/create only
- Lead-to-deal conversion using `POST /leads/{lead_id}/convert`
- Responsive desktop sidebar, mobile navigation, forms, tables, status badges, and error states
- User role restrictions in the UI that mirror backend access rules; backend remains authoritative

## Requirements

- Node.js 20+ recommended
- Existing CRM backend running and database migrated

## Run locally

1. Start the backend from its project directory:

   ```bash
   uvicorn app.main:app --reload
   ```

2. In this directory, create `.env` from `.env.example` and adjust `VITE_API_BASE_URL` if needed.
3. Install and run the frontend:

   ```bash
   npm install
   npm run dev
   ```

4. Open the Vite URL shown in the terminal, usually `http://localhost:5173`.

## Backend API alignment

Base URL default: `http://127.0.0.1:8000/api/v1`

- `/auth/register` — `name`, `email`, `password`
- `/auth/login` — JSON `email`, `password`; response includes `access_token`, `token_type`
- `/auth/me` — current profile
- `/dashboard/summary` — backend-provided dashboard metrics
- `/users`, `/companies`, `/contacts`, `/leads`, `/deals`, `/activities`, `/tasks`

The backend's register schema does not accept a role field. Public registration therefore does not expose role selection. The backend determines the role. Admin-only user management calls `/users`.

## Important notes

- Ensure the backend CORS configuration permits the Vite origin, usually `http://localhost:5173`. Set `CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173` in the backend environment if required, then restart it.
- The backend uses `401` for missing/invalid authentication and the frontend returns to login on a `401` response.
- The backend's current activity API only supports list, detail, and create. The frontend intentionally does not offer activity editing or deletion.
- This frontend does not add admin approval endpoints, company passkeys, or any backend functionality not present in the supplied source.
- Dashboard figures come from the backend summary endpoint. The frontend does not fabricate chart data.
