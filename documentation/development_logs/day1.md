## Tasks Day 1: Wednesday (1/2 day)

## (30 min) Brainstorm

**Description:** Write a quick system design with the first thing that come to my mind. Identify key decision points, and areas to deep dive so I can create new tasks.

- Db: structure or non structure db
- How does a transcription looks like? I need real examples

## (15 min) Defined Functional and Non-Functional Requirements

- The function requirements are given in the task description
- Non functional:

  1. It needs to be scalable
  2. It needs to be async because the transcription can take time
  3. Handle errors

## (1 hr) Improve the System Design Description

**Description:** Explain the reasoning behind each decision

### System Design

It needs to be async, with multiple services to ensure scalability. Each service must be contained in its own docker container.

**MVP**

| Service          | Priority | Notes                                                                 |
| ---------------- | -------- | --------------------------------------------------------------------- |
| Backend Api      | High     | Simple but robust                                                     |
| Client interface | Low      | It can be as simple as a Swagger                                      |
| Database         | High     | Key decision here!                                                    |
| Broker           | Medium   | Key part of the system to ensure async behaviour, simple setup ideal  |
| Worker           | Medium   | Need to scale horizontally; mocked output, focus on broker connection |
| Monitoring       | Low      | Check the db, use existing services                                   |

**Backend API**

- **Python + FastAPI:**  
  Fast, easy to develop, it creates Swagger files automatically and I feel comfortable with it

- **Uv for package and env management:**  
  Fast and well documented

- **Pytest for tests**

**Client Interface**

- For the FE we will use the OpenAPI (`/docs`) generated automatically.

⚠️ **Risk:** it might not be the most intuitive UI, but this is an MVP so I prefer to focus on the functional aspect of the challenge

**DB**

- **Key decision point:** PostgreSQL

- **Why**:
  - The data will not change often
  - I can use structured queries to fetch data
  - PostgreSQL has full-text search
  - it can be easily monitored using PG admin

_For this MVP, the data to store will be only text, not images._

**Broker**

- **Redis:**  
  Easy and quick setup. If I have more time I can use something better like RabbitMQ, but this will not be a priority

**Worker**

Simple celery queues to handle the events.

- **Why**:
  - Celery is simple and flexible
  - it provides a nice ui to check the events that will be useful

## Create development tasks

the focus of this day will be to set up the different services

goal: have a docker-compose with all the services + some simple code to ensure each service runs

dtk -> development task number( this naming convetion will be useful for the branches)

- dtk01 (10 min): set up the fastApi app with simple endpoint ✅
  - use the uv documentation as a guide
- dtk02 (15 min): run the fastApi inside a container ✅
- dtk03 (1 hr ): set up the postgress db + pgadmin ✅
  - create docker-compose with the db and include the docker file of the fastApi app ✅
  - create basic models for the tables ✅
  - ensure the fast api app can reach the db ✅

Notes:

1. I encountered some issues with the timing between FastAPI and the database initialization. I resolved these by adding a health check in the Docker Compose configuration.

2. Designing the database structure took longer than expected (+ 1 hr) due to additional considerations. As a result, I need to re-estimate the tasks related to the broker and consumers, which I will move to tomorrow.

- dtk04 (20 min): setup the broker
- dtk05 (1 hr min): set up the worker + celery
  - make sure it consumes the events
