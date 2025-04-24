from fastapi import APIRouter, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from uuid import uuid4
from app.celery.transcription_worker_client import celery_app
from fastapi import Depends
from ..database.database import get_db
from app.services.transcription_service import enqueue_transcription_task
from app.repositories.video_repository import add_video_record, fetch_video_and_transcription
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


@router.post("/transcribe", response_model=TranscribeResponse, status_code=202)
async def transcribe(request: TranscribeRequest, db: db_dependency):
    try:
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
    except SQLAlchemyError as e:
        print(f"[ERROR] Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error while processing transcription")
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Unexpected error while processing transcription")


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
    except SQLAlchemyError as e:
        print(f"[ERROR] Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error while fetching transcription")
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Unexpected error while fetching transcription")
