# Appointment Management System API

This service provides the backend API for appointment management. It includes endpoints
for managing users and appointments, and is designed to be small, testable, and
easy to extend.

Current endpoints (high level):

- `POST /users/` — create a user (email must be unique).
- `GET /users/{id}` — fetch user by id.

Guidelines:

- Keep this OpenAPI description accurate when adding or changing endpoints.
- Use Pydantic models for request/response schemas so they appear in OpenAPI.
- Version breaking changes under `/api/v1/` and increment the API version.
