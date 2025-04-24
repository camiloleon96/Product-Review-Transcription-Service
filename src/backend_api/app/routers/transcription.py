from fastapi import APIRouter, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from uuid import uuid4
from app.trascription_worker_client import celery_app
from fastapi import Depends
from ..database.database import get_db
from app.models.models import Video, Transcription, TranscriptionStatus
from app.schemas.transcription_schemas import (
    TranscribeRequest,
    TranscribeResponse,
    TranscriptionResponse,
)

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix='/video',
    tags=['video']
)

def add_video_record(db, video_id, video_url):
    try:
        db_video = Video(
            id=video_id,
            transcription_status=TranscriptionStatus.pending,
            url=video_url,
        )
        db.add(db_video)
        db.commit()
        db.refresh(db_video)
        return db_video
    except SQLAlchemyError as e:
        db.rollback()  
        print(f"[ERROR] Database error while inserting video: {e}")
        raise HTTPException(status_code=500, detail="Database error while inserting video")
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Unexpected error while inserting video: {e}")
        raise HTTPException(status_code=500, detail="Unexpected error while inserting video")

def enqueue_transcription_task(celery_app, video_id, video_url):
    try:
        print(f"[QUEUE] Enqueued transcription task for video_id={video_id}")
        celery_app.send_task("celery_worker.transcribe_video", args=[video_id, video_url])
    except Exception as e:
        print(f"[ERROR] Failed to enqueue transcription task: {e}")
        raise HTTPException(status_code=500, detail="Failed to enqueue transcription task")


@router.post("/transcribe", response_model=TranscribeResponse, status_code=202)
async def transcribe(request: TranscribeRequest, db: db_dependency):
    video_url = str(request.url)
    video_id = str(uuid4())

    print(f"[DB] Insert video: id={video_id}, url={video_url}, status='pending'")

    add_video_record(db, video_id, video_url)
    enqueue_transcription_task(celery_app, video_id, video_url)

    return TranscribeResponse(
        video_id=video_id,
        status="pending",
        message="Transcription in progress. Use GET /transcription/{video_id} to check status."
    )


def fetch_video_and_transcription(db: Session, video_id: str):
    """
    Fetch video and transcription data for a given video_id.
    """
    result = db.query(
        Video.id.label("video_id"),
        Video.title,
        Video.url,
        Video.language,
        Video.transcription_status,
        Video.uploaded_at,
        Transcription.transcribed_text,
        Transcription.created_at.label("transcription_created_at")
    ).outerjoin(
        Transcription, Video.id == Transcription.video_id
    ).filter(
        Video.id == video_id
    ).first()

    if not result:
        return None

    return {
        "video_id": result.video_id,
        "title": result.title,
        "url": str(result.url),
        "language": result.language,
        "transcription_status": result.transcription_status,
        "uploaded_at": result.uploaded_at,
        "transcribed_text": result.transcribed_text,
        "transcription_created_at": result.transcription_created_at,
    }
@router.get("/transcription/{video_id}", response_model=TranscriptionResponse)
async def get_transcription(video_id: str, db: db_dependency):
    try:
        print(f"[DB] Fetch transcription for video_id={video_id}")
        transcription = fetch_video_and_transcription(db, video_id)
        if not transcription:
            raise HTTPException(status_code=404, detail="Video not found")
        return TranscriptionResponse(
            video_id=video_id,
            title=transcription["title"],
            url=transcription["url"],
            status=transcription["transcription_status"],
            language=transcription["language"],
            transcription=transcription["transcribed_text"],
        )
    except HTTPException as e:
        print(f"[ERROR] HTTP exception: {e.detail}")
        raise e
    except SQLAlchemyError as e:
        print(f"[ERROR] Database error: {e}")
        raise HTTPException(status_code=500, error="Database error while fetching transcription")
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        raise HTTPException(status_code=500, error="Unexpected error while fetching transcription")
