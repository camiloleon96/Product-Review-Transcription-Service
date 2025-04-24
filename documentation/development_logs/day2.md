## Tasks Day21: Thursday

yesterday while setting up the db I realized I needed to improve the overall flow. The issue is that the worker might take some time to transcribe the video. Thats why I'll implement a polling mechanism. showed in ../diagrams/transcription_flow

---

the focus of this day will be to develop the api and the worker, design the messages interfaces

goal:

- work int the documentation
- finish seting up the docker compose
- have a first version of the endpoint ready
- have the worker mocking the transcriptions

## dtk04 (20 min): setup the broker

- create the docker file for the redis

## dtk05 (1hr): set up the worker + celery

- implement layout for the transcription endpoints (define the schemas) so I can start testing the broke with some mock transcription requests
-
