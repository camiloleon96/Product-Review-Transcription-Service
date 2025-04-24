import os
import time
import uuid

from celery import Celery
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

load_dotenv()

celery = Celery(__name__)
celery.conf.broker_url = os.getenv("CELERY_BROKER_URL")
celery.conf.result_backend = os.getenv("CELERY_RESULT_BACKEND")

# Setup Db connection
DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

@celery.task
def transcribe_video(video_id: str, youtube_url: str):
    print(f"[Worker] Transcribing: {youtube_url} (video_id={video_id})")
    session = SessionLocal()
    try:
        # Insert into videos with initial status "pending"
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

        # Simulate processing
        time.sleep(5)

        # Insert transcription text
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

        # Update video status to "completed"
        update_status_sql = text("""
            UPDATE videos SET transcription_status = :transcription_status WHERE id = :id
        """)
        session.execute(update_status_sql, {
            "id": video_id,
            "transcription_status": "completed"
        })
        session.commit()

        print(f"[Worker] Done: {video_id}")

    except Exception as e:
        session.rollback()
        print(f"[Worker] Error: {e}")
    finally:
        session.close()
