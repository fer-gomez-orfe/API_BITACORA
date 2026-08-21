# Vehicle Usage Management API

REST API developed with **FastAPI** for managing the usage of company vehicles.

This backend is part of the **Vehicle Usage Management** project, an Android application designed to register and track vehicle usage by employees, including authentication, vehicle information and usage records.

> 🚧 **Project Status:** In Development

---

## 📌 About the Project

The project was created to replace a previous vehicle usage registration solution with a more structured client-server architecture.

The system consists of:

- An **Android application** developed with Kotlin.
- A **REST API** developed with FastAPI.
- A **SQLite database** for persistent data storage.
- **JWT authentication** for user sessions and protected API requests.

The API manages user authentication, vehicle availability and the complete vehicle usage lifecycle, from checkout registration to vehicle return and user-specific usage history.

---

## 🛠 Tech Stack

- **Python**
- **FastAPI**
- **SQLModel**
- **SQLite**
- **JWT Authentication**
- **Uvicorn**

---

## ✨ Current Features

- User registration and authentication.
- JWT-based access control.
- Authenticated user profile retrieval.
- Vehicle creation and retrieval.
- Available vehicle filtering.
- Vehicle checkout registration.
- Vehicle return registration.
- Active usage record retrieval.
- User-specific vehicle usage history.
- SQLite persistence through SQLModel.
- Interactive API documentation with Swagger UI and ReDoc.

---

## 🔐 Authentication

The API uses **JWT-based authentication**.

After a successful login, the API returns an access token:

```json
{
  "access_token": "<token>",
  "token_type": "bearer"
}
```

The token must be included in protected requests using the Authorization header:

```http
Authorization: Bearer <access_token>
```

The Android client stores the token locally and automatically attaches it to authenticated API requests.

---

## 📡 API Endpoints

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/auth/signup` | Register a new user |
| `POST` | `/auth/login` | Authenticate a user and generate a JWT access token |
| `GET` | `/auth/me` | Retrieve the authenticated user's information |

### Vehicles

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/vehicles/` | Retrieve all vehicles |
| `POST` | `/vehicles/` | Create a new vehicle |
| `GET` | `/vehicles/available` | Retrieve currently available vehicles |

### Vehicle Usage Records

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/records/register/out` | Register a vehicle checkout |
| `POST` | `/records/register/return/{register_id}` | Register the return of a vehicle |
| `GET` | `/records/active/records` | Retrieve active vehicle usage records |
| `GET` | `/records/my/records` | Retrieve the authenticated user's usage history |

### General

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | API root endpoint |

---

## 🏗 Project Architecture

The backend separates API routes, database models and application logic to keep responsibilities organized.

A simplified request flow is:

```text
Android Application
        │
        │ HTTP / REST
        ▼
     FastAPI
        │
        ├── Authentication
        ├── Users
        ├── Vehicles
        └── Usage Records
        │
        ▼
     SQLModel
        │
        ▼
      SQLite
```

---

## 🚀 Running the Project

### 1. Clone the repository

```bash
git clone https://github.com/fer-gomez-orfe/vehicle-usage-management-api.git
cd vehicle-usage-management-api
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows**

```bash
.venv\Scripts\activate
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the development server

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

> The exact command may vary depending on the current project structure.

---

## 📖 API Documentation

Once the server is running, interactive documentation is available at:

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

```

provides the Swagger UI documentation.

The alternative ReDoc documentation is available at:

```text
/redoc
```

---

## 📱 Android Client

The API is designed to work with the **Vehicle Usage Management Android App**.

The Android application is being developed with:

- Kotlin
- Jetpack Compose
- Material 3
- MVVM
- Clean Architecture
- Hilt
- Retrofit
- OkHttp
- Coroutines
- StateFlow

The Android repository will be linked here once it is published.

---

## 🗺 Roadmap

- [x] User registration
- [x] User authentication
- [x] JWT access tokens
- [x] Authenticated user endpoint
- [x] Vehicle creation and retrieval
- [x] Available vehicle retrieval
- [x] Vehicle checkout registration
- [x] Vehicle return registration
- [x] Active vehicle usage records
- [x] User vehicle usage history
- [x] SQLite persistence
- [ ] Improve error handling and validation
- [ ] Add automated tests
- [ ] Add refresh-token strategy
- [ ] Add CI/CD workflow
- [ ] Complete Android client integration

---

## 🎯 Project Goals

This project is being developed both as a practical internal-use solution and as a way to apply modern software development practices, including:

- REST API design
- Authentication and authorization
- Client-server architecture
- Separation of responsibilities
- Mobile/backend integration
- Database modeling
- Error handling
- Automated testing

---

## 👤 Author

**Fernando Gómez García**

Software & Integration Engineer  
Android · Kotlin · REST APIs · SQL · IoT Solutions