# Finance Data Processing and Access Control Backend

## Project Overview
The Finance Data Processing and Access Control Backend is a robust, modular, and production-ready API designed to securely manage financial records and compute dynamic dashboard analytics while enforcing seamless, role-based access control.

## Features
*   **Structured API Responses:** Complete standardized `{"status", "message", "data"}` API JSON replies.
*   **Advanced Data Fetching:** Includes granular structural pagination returning complete dataset counts, offset indexing limits, and complex cross-column `OR` search operations.
*   **Security & Stability:** Defended fully by `slowapi` ensuring 60 requests per minute boundaries across data layers preventing malicious bursts.
*   **Test Driven:** Bootstrapped fully against comprehensive `pytest` assertions verifying CRUD access, memory limits, and logic validations natively.
*   **Strict Validations:** Converts typical unprocessable anomalies (like bad Date schemas) organically into 400 Bad Request handlers improving integration logic.

## Tech Stack
*   **Language:** Python 3
*   **Web Framework:** FastAPI
*   **Database ORM:** SQLAlchemy
*   **Database:** SQLite
*   **Validations:** Pydantic
*   **Rate Limiting:** SlowAPI
*   **Testing:** Pytest / httpx

## Project Architecture
The underlying engine isolates components precisely using robust architectural paradigms perfectly equipped for Serverless scaling on Railway:
*   `main.py`: Houses FastAPI lifespan configuration orchestrating routers and dependencies.
*   `routes/`: Clean abstraction isolating logic strictly mapped to endpoints utilizing precise `FastAPI` Swagger properties.
*   `services/`: Centralizes the entire SQLAlchemy query definitions cleanly decoupled from routes.
*   `schemas.py`: Maps complex recursive `Generics` guaranteeing the API's payloads map correctly.
*   `tests/`: End-to-end simulated HTTP Clients integrated tightly against an in-memory db preventing pollution.

## RBAC Roles Explanation

The system leverages FastAPI `Depends` components to verify headers and handle authorization layers fluidly. Since we are circumventing typical token integrations (like JWT) for simpler logic, we are relying on an HTTP request Header labeled `X-User-Id`. 

The system implements strict permission cascades:
*   **Viewer:** Can only read analytic summaries and lookup existing records.
*   **Analyst:** Operates identically to the Viewer role.
*   **Admin:** Has complete execution coverage over system features; the sole entity able to add, modify, or drop records and users.

## API Endpoints

*   **`/users`**
    *   `POST /users/`: Create User (Admin Only)
    *   `GET /users/`: Get All Users (Admin Only)
*   **`/records`**
    *   `POST /records/`: Create a Record (Admin Only)
    *   `GET /records/`: Fetch/Filter Records (Supports `search`, `start_date`, `end_date`, `type`, `category`, and strict payload pagination `page`/`limit`) (Viewer or higher)
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

## Deployment Instructions
The application is pre-configured and securely deployable on standard cloud container environments like Railway.

1.  **Clone the Repository locally (or hook to Railway source logic).**
2.  **Environment Dependencies:** Keep the native SQLite logic if ephemeral state is acceptable, or hook a Postgres Engine String to `DATABASE_URL` configurations natively mapped in `database.py`.
3.  **Procfile / Launch Commands:** Start Uvicorn pointing tightly against the web engine:
    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port $PORT
    ```

## Live API Documentation
You can seamlessly interface with the real-time deployed API directly through the live, interactive Swagger Documentation!

🔗 **[Live API Playground: https://finance-backend-production-0ef3.up.railway.app/docs](https://finance-backend-production-0ef3.up.railway.app/docs)**
