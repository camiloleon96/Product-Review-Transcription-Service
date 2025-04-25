# Project Management and Timeline

The project began with a 2-hour ideation phase focused on brainstorming initial ideas, sketching out a rough system design based on first impressions, and progressively refining it. During this session, I also identified key priorities to better understand where to allocate more time and effort. This helped in narrowing the scope of the system in alignment with the requirements and led to the creation of the initial task list, including rough time estimates for each item.

As a result of this initial phase, I created a clear set of tasks and main goals for the first 3 days of development, along with a future roadmap to guide ongoing progress and improvements.

### Day 1 (Wednesday) — Setup Phase

- dtk01: Set up FastAPI app
- dtk02: Run FastAPI in Docker
- dtk03: Setup PostgreSQL + pgAdmin, initial schema
- dtk04: Setup Redis broker
- dtk05: Setup Celery worker (mock transcription)

### Day 2 (Thursday) — Coding Phase

- Implement polling flow for GET transcription
- dtk06: Complete GET endpoint and refactor schemas
- Add unit tests

### Day 3 (Friday) — Documentations

- Finish all the deliverables

### ⚠️ Risks and Mitigation

| Risk                   | Mitigation Strategy                         |
| ---------------------- | ------------------------------------------- |
| Non-intuitive UI       | Use OpenAPI docs as stop-gap                |
| Celery task failures   | Retry policies and task monitoring (Flower) |
| Service startup timing | Healthchecks and service dependency config  |

### Future Roadmap (Improvements)

- Implement retry logic for failed tasks
- Frontend client for better UI
- Replace polling with WebSockets for real-time status
- Use kubernates for a proper scaling machanism
- Replace mock transcription with a real integration

## Progress

The initial tasks served as a helpful guideline throughout development, but as I progressed, I encountered a few issues and identified areas in the workflow that needed refinement. While I was able to meet the main goals set for each day, new tasks emerged along the way, and some existing ones expanded as I gained a better understanding of where improvements could be made. However, due to time constraints and the defined scope of the MVP, not all enhancements could be implemented at this stage.

### Day 1 Summary

| Task ID | Task Description                              | Time Spent | Status  | Notes                                                             |
| ------- | --------------------------------------------- | ---------- | ------- | ----------------------------------------------------------------- |
|         | Ideation phase                                | 2 hr       | ✅      | Created a first version of the system, and chose the technologies |
| dtk01   | Set up the FastAPI app with a simple endpoint | 10 min     | ✅      | Used the `uv` documentation as a guide.                           |
| dtk02   | Run the FastAPI app inside a Docker container | 15 min     | ✅      | Successfully containerized the FastAPI app.                       |
| dtk03   | Set up PostgreSQL database and PGAdmin        | 2 hr       | ✅      | Created Docker Compose with FastAPI and DB. Ensured connectivity. |
|         | - Created basic models for database tables    |            | ✅      | Took extra time to design the database structure (+1 hr).         |
|         | - Added health checks for DB initialization   |            | ✅      | Resolved timing issues between FastAPI and DB initialization.     |
| dtk04   | Set up the broker (Redis)                     | 20 min     | started | Chose Redis for simplicity and quick setup.                       |

**Total Time Spent: ~5 hrs**

### Day 2 Summary

| Task ID       | Task Description                                   | Time Spent | Status | Notes                                                                   |
| ------------- | -------------------------------------------------- | ---------- | ------ | ----------------------------------------------------------------------- |
| dtk04         | Reworked the data flow                             | 1 hr       | ✅     | decided to go for a polling mechanism to check the transcription status |
| dtk04         | Set up the broker (Redis)                          | 20 min     | ✅     | Created the Dockerfile for Redis and ensured it works with the worker.  |
| dtk05         | Set up the worker with Celery and Flower dashboard | 1 hr       | ✅     | Mocked transcription logic and updated the transcription in the DB.     |
|               | - Defined schemas for transcription endpoints      |            | ✅     | Created schemas to test the broker with mock transcription requests.    |
|               | - Identified missing product data in DB design     |            | ✅     | Realized the need to include product data in the DB.                    |
| hotfix        | Updated DB models to include product data          | 1 hr       | ✅     | Added a junction table for video-product relationships.                 |
| dtk06         | Implement the GET transcriptions endpoint          | 5 hr       | ✅     | Refactored schemas and implemented basic unit tests.                    |
|               | - Wrote unit tests for the endpoint                |            | ✅     | Faced issues with DB mocking but resolved enough for MVP.               |
|               | - Refactored code structure                        |            | ✅     |                                                                         |
| Documentation | Write about areas for improvement                  | 30 min     | ✅     | Documented potential improvements and assumptions for the MVP.          |

**Total Time Spent: ~9 hr**

### Day 3 Summary

| Task ID       | Task Description        | Time Spent | Status | Notes                                                          |
| ------------- | ----------------------- | ---------- | ------ | -------------------------------------------------------------- |
| Documentation | Finish the deliverables | 2 hr       | ✅     | Used the unnredacted development logs to create the final docs |

**Total Time Spent: ~2 hr**

## Future Roadmap (Updated)

- Properly configure Ruff for Python, or set it up with pre-commit
- Fix and improve the health check in the docker-compose setup
- Refactor the code to use abstract classes, making it easier to migrate to other technologies in the future
- Use TSVECTOR for transcription search optimization (currently commented out in the model definition)
- Add CRUD API for the product entity: although not currently used, the database schema already supports a product-to-video relationship via a junction table. A product can appear in multiple videos, and a video can contain multiple products
- Implement retry logic for failed tasks
- Develop a frontend client for a better UI (e.g., React or Next.js)
- Replace polling with WebSockets for real-time status updates
- Use Kubernetes for scalable deployment, or consider moving to a cloud service
