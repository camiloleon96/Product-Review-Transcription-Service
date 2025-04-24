import os
import time
import uuid

from celery import Celery
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Load environment variables
load_dotenv()

# Setup Celery
celery = Celery(__name__)
celery.conf.broker_url = os.getenv("CELERY_BROKER_URL")
celery.conf.result_backend = os.getenv("CELERY_RESULT_BACKEND")

# Setup database connection
DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def insert_video(session, video_id: str, youtube_url: str):
    insert_video_sql = text("""
        INSERT INTO videos (id, url, title, language, transcription_status)
        VALUES (:id, :url, :title, :language, :transcription_status)
    """)
    session.execute(insert_video_sql, {
        "id": video_id,
        "url": youtube_url,
        "title": "Mock Video Title",
        "language": "en",
        "transcription_status": "pending"
    })
    session.commit()


def insert_transcription(session, video_id: str):
    insert_transcription_sql = text("""
        INSERT INTO transcriptions (id, video_id, transcribed_text)
        VALUES (:id, :video_id, :text)
    """)
    session.execute(insert_transcription_sql, {
        "id": str(uuid.uuid4()),
        "video_id": video_id,
        "text": "This is a mock transcription of the video content."
    })
    session.commit()


def update_video_status(session, video_id: str, status: str):
    update_status_sql = text("""
        UPDATE videos SET transcription_status = :status WHERE id = :id
    """)
    session.execute(update_status_sql, {
        "id": video_id,
        "status": status
    })
    session.commit()


@celery.task
def transcribe_video(video_id: str, youtube_url: str):
    print(f"[Worker] Transcribing: {youtube_url} (video_id={video_id})")
    session = SessionLocal()
    try:
        insert_video(session, video_id, youtube_url)

        time.sleep(5)  # simulate processing

        insert_transcription(session, video_id)
        update_video_status(session, video_id, "completed")

        print(f"[Worker] Done: {video_id}")
    except Exception as e:
        session.rollback()
        print(f"[Worker] Error: {e}")
    finally:
        session.close()
