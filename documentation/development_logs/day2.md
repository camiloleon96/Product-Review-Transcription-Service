## Tasks Day21: Thursday

yesterday while setting up the db I realized I needed to improve the overall flow. The issue is that the worker might take some time to transcribe the video. Thats why I'll implement a polling mechanism. showed in ../diagrams/transcription_flow

---

The focus of this day will be to develop the backend, the worker, and design the message interfaces

**Goals:**

- work in the documentation
- finish setting up the docker compose
- have the worker mocking the transcriptions (dtk05 ✅ )
- have a first version of the endpoint ready (dtk06 ✅ )

## dtk04 (20 min): setup the broker

- create the docker file for the redis

## dtk05 (2hr): set up the worker + celery (and flower dashboard)

- implement layout for the transcription endpoints (define the schemas) so I can start testing the broke with some mock transcription requests
- implement mocked logic to updte the transcription in the Db

while developing this I realized there is something missing in the db desing: the product data

## Create more development tasks ✅

Now, the focus will be on the development of the api and update the db design and document everything.

- hotfix: db models to include product data ✅
- dtk06 (2 hr): implement the GET transcriptions endpoint✅
  - while working in this I can refactor some other things that are pending for example refactor the schemas
  - write unit tests ✅(implemented some basic ones, needed more time to figure out an issue with the db mock, but for a mvp is ok I think)
- documentation: write about the things that can be improved

## hotfix dbmodels ✅

assumption: for the following mvp, one video will contain the review of only one product, however the db will be compatible to handle:
One video -> many products
one product -> many videos
The video_products table is a junction table, because the score is given by each video

## dtk06 (3 hr) ✅
