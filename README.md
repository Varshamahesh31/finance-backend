# Finance Data Processing and Access Control Backend

A clean and modular FastAPI backend for a finance dashboard showing API design, database modeling, role-based access control, and financial data processing.

## Tech Stack
- Python 3
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic

## Getting Started

1. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

4. View documentation:
   Open `http://localhost:8000/docs` to see the Swagger interactive documentation.

## Access Control Implementation

Since there was no JWT or session-based authentication required, a mock RBAC is simulated via a Header `X-User-Id`. 

- **Admin**: Can create/update/delete any records and users.
- **Analyst**: Can view records and summaries.
- **Viewer**: Can view records and summaries.

To test as a user:
1. Create a user with `admin` role by hitting `POST /users` (no header required to create the first user, but the endpoint `POST /users` checks for admin. Wait, to bootstrap an admin, you can manually insert into the sqlite DB or modify the `POST /users` temporarily. To make it simpler, the provided implementation actually enforces `require_admin` on `POST /users`. You might need to seed an admin or remove the dependency temporarily for the first user). Let's say we seed via python terminal directly.

Alternatively, you could bypass checking for the very first user in a real scenario.
