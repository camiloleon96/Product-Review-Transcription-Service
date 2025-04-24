import os
import time

from celery import Celery
from dotenv import load_dotenv

load_dotenv()

celery = Celery(__name__)
celery.conf.broker_url = os.getenv("CELERY_BROKER_URL")
celery.conf.result_backend = os.getenv("CELERY_RESULT_BACKEND")


@celery.task
def transcribe_video(video_id: str, youtube_url: str):
    print(f"[Worker] Transcribing: {youtube_url} (video_id={video_id})")
    time.sleep(5)
    print(f"[Worker] Done: {video_id}")

# print("Check the key for the queue")
# print(celery.tasks.keys())