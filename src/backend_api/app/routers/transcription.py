from fastapi import APIRouter, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session
from uuid import uuid4
from app.trascription_worker_client import celery_app
from fastapi import Depends
from ..database.database import get_db
from app.models.models import Video, TranscriptionStatus
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
    video_id = str(uuid4())

    print(f"[DB] Insert video: id={video_id}, url={request.url}, status='pending'")
    db_video=Video(
     id=video_id,
     transcription_status= TranscriptionStatus.pending,
     url=str(request.url),
    )

    try:
        db.add(db_video)
        db.commit()
        db.refresh(db_video)
    except Exception as e:
        db.rollback()  
        print(f"[ERROR] Failed to insert video entry: {e}")
        raise HTTPException(status_code=500, detail="Failed to create video entry in database")

    print(f"[QUEUE] Enqueued transcription task for video_id={video_id}")
    celery_app.send_task("celery_worker.transcribe_video", args=[video_id, str(request.url)])

    return TranscribeResponse(
        video_id=video_id,
        status="pending",
        message="Transcription in progress. Use GET /transcription/{video_id} to check status."
    )

@router.get("/transcription/{video_id}", response_model=TranscriptionResponse)
async def get_transcription(video_id: str):
    print(f"[DB] Fetch transcription for video_id={video_id}")

    return TranscriptionResponse(
        video_id=video_id,
        title="Mocked Product Review Video",
        url="https://youtube.com/watch?v=mock123",
        status="transcribed",
        transcription="this is a mocked transcription bla, bla, bla..."
    )
