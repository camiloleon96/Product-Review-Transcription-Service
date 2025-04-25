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


def update_video_metadata(session, video_id: str):
    update_video_sql = text("""
        UPDATE videos
        SET title = :title,
            language = :language,
            transcription_status = :transcription_status
        WHERE id = :id
    """)

    session.execute(update_video_sql, {
        "id": video_id,
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
    avocado_peeler_review = """
        [Intro music fades]
        Reviewer:
        "Hey everyone! Today I’m testing out this 3-in-1 avocado peeler. Let’s see if it’s worth the hype."
        [Cuts avocado]
        Reviewer:
        "Okay, the slicer part? Super smooth. It glides right through. No mess, no fuss."
        [Scooping and slicing]
        Reviewer:
        "The pitter works too—just press and twist, and boom, pit's out! And these slices? Look at that—perfect every time."
        [Holds it up to the camera]
        Reviewer:
        "If you eat avocados weekly like I do, this thing’s a game-changer. Highly recommend."
        [Outro music]
        """

    insert_transcription_sql = text("""
        INSERT INTO transcriptions (id, video_id, transcribed_text)
        VALUES (:id, :video_id, :text)
    """)
    session.execute(insert_transcription_sql, {
        "id": str(uuid.uuid4()),
        "video_id": video_id,
        "text": avocado_peeler_review
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
        update_video_metadata(session, video_id)

        time.sleep(10)  # simulate processing

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
