import os
import time
import uuid

from celery import Celery
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import random

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


def insert_product(session) -> str:
    product_id = str(uuid.uuid4())
    sql = text("""
        INSERT INTO products (id, product_name, brand_name, category)
        VALUES (:id, :product_name, :brand_name, :category)
    """)
    session.execute(sql, {
        "id": product_id,
        "product_name": "Mock Product",
        "brand_name": "Mock Brand",
        "category": "Mock Category"
    })
    session.commit()
    return product_id


def insert_video_product(session, video_id: str, product_id: str):
    sql = text("""
        INSERT INTO video_products (id, video_id, product_id, score)
        VALUES (:id, :video_id, :product_id, :score)
    """)
    session.execute(sql, {
        "id": str(uuid.uuid4()),
        "video_id": video_id,
        "product_id": product_id,
        "score": random.randint(1, 10)
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

        product_id = insert_product(session)
        insert_video_product(session, video_id, product_id)

        update_video_status(session, video_id, "completed")

        print(f"[Worker] Done: {video_id}")
    except Exception as e:
        session.rollback()
        print(f"[Worker] Error: {e}")
    finally:
        session.close()
