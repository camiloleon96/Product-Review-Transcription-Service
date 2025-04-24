from fastapi import APIRouter
from typing import Annotated
from sqlalchemy.orm import Session
from uuid import uuid4
from app.trascription_worker_client import celery_app
from fastapi import Depends
from ..database.database import get_db
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
async def transcribe(request: TranscribeRequest):
    video_id = str(uuid4())

    print(f"[DB] Insert video: id={video_id}, url={request.url}, status='pending'")

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
