# Finance Data Processing and Access Control Backend

## Project Overview
The Finance Data Processing and Access Control Backend is a robust, modular, and production-ready API designed to securely manage financial records and compute dynamic dashboard analytics while enforcing seamless, role-based access control.

## Tech Stack
*   **Language:** Python 3
*   **Web Framework:** FastAPI
*   **Database ORM:** SQLAlchemy
*   **Database:** SQLite
*   **Validation Validation:** Pydantic

## Setup Instructions

Ensure you have Python installed on your system (Python 3.9+ recommended).

1.  **Clone the repository locally.**
2.  **Initialize a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # macOS / Linux
    # .\venv\Scripts\activate # Windows
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Running the Server

To start the FastAPI development server, use Uvicorn configured for module watching:
```bash
uvicorn app.main:app --reload
```
The server will now be listening by default on `http://localhost:8000`.

*   **API Root:** `http://localhost:8000/`
*   **Live Swagger Docs:** `http://localhost:8000/docs`

> **Note:** Upon the server starting, the `lifespan` event automatically ensures that a default Admin user (`admin@test.com`) is injected into the database if one does not exist.

## API Endpoints Overview

*   **`/users`**
    *   `POST /users/`: Create User (Admin Only)
    *   `GET /users/`: Get All Users (Admin Only)
*   **`/records`**
    *   `POST /records/`: Create a Record (Admin Only)
    *   `GET /records/`: Fetch/Filter Records (Supports `start_date`, `end_date`, `type`, `category`, and pagination with `page`/`limit`) (Viewer or higher)
    *   `GET /records/{record_id}`: Read single record (Viewer or higher)
    *   `PUT /records/{record_id}`: Update specific record (Admin Only)
    *   `DELETE /records/{record_id}`: Destroy specific record (Admin Only)
*   **`/summary`**
    *   `GET /summary/income`: Total logged income
    *   `GET /summary/expense`: Total logged expense
    *   `GET /summary/balance`: Real-time net balance
    *   `GET /summary/category`: Value distributions grouped by category 
    *   `GET /summary/recent`: The 10 most recent chronological records
    *   `GET /summary/monthly`: Income/Expense trends isolated historically by month.

*(Check the Live Swagger Docs for detailed schemas, inputs, and response bodies.)*

## Role Based Access Control (RBAC)

The system leverages FastAPI `Depends` components to verify headers and handle authorization layers fluidly. Since we are circumventing typical token integrations (like JWT) for simpler logic, we are relying on an HTTP request Header labeled `X-User-Id`. 

The system implements strict permission cascades:
*   **Viewer:** Can only read analytic summaries and lookup existing records.
*   **Analyst:** Operates identically to the Viewer role.
*   **Admin:** Has complete execution coverage over system features; the sole entity able to add, modify, or drop records and users.

## Example Request Headers

Injecting the User ID manually implies mocking the logged-in user state. The Application provides a bootstrapped default Admin assigned typically to ID `1`. 

To run an Admin operation (like creating a record):
```http
X-User-Id: 1
```

## Example API Usage

**Creating a new record using Curl:**
```bash
curl -X 'POST' \
  'http://localhost:8000/records/' \
  -H 'accept: application/json' \
  -H 'X-User-Id: 1' \
  -H 'Content-Type: application/json' \
  -d '{
  "amount": 250.50,
  "type": "expense",
  "category": "Software Subscriptions",
  "date": "2026-04-15",
  "notes": "Annual Cloud Hosting Bill",
  "user_id": 1
}'
```

**Fetching records with filters:**
```bash
curl -X 'GET' \
  'http://localhost:8000/records/?type=expense&start_date=2026-04-01&end_date=2026-04-30&page=1&limit=5' \
  -H 'accept: application/json' \
  -H 'X-User-Id: 1'
```
