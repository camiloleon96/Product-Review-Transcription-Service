## High-level design

<img src="./diagrams/hld.png" alt="High-level Design" width="500"/>

## Flow diagram

<img src="./diagrams/transcription_flow.png" alt="High-level Design" width="500"/>

## Database schema

<img src="./diagrams/database_schema.png" alt="High-level Design" width="500"/>

## Backend Api: folder structure

```python
src/backend_api
├── app/
│ ├── routers/ # API route handlers
│ │ └── transcription.py
│ ├── services/ # Business logic
│ │ └── transcription_service.py
│ ├── repositories/ # Database operations
│ │ └── video_repository.py
│ ├── models/ # SQLAlchemy models
│ │ └── models.py
│ ├── schemas/ # Pydantic schemas
│ │ └── transcription_schemas.py
│ ├── celery/ # Celery tasks
│ │ └── transcription_worker_client.py
│ ├── database/ # Database connection
│ │ └── database.py
│ └── main.py # FastAPI app entry point
├── tests/
│ ├── routers/
│ │ └── test_transcription.py
| └── test_main.py
```
