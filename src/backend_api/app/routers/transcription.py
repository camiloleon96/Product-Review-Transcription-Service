from fastapi import APIRouter
from pydantic import BaseModel, HttpUrl
from uuid import uuid4

router = APIRouter()

# TODO: move this to a separate file

class TranscribeRequest(BaseModel):
    url: HttpUrl

class TranscribeResponse(BaseModel):
    video_id: str
    status: str
    message: str

class Segment(BaseModel):
    start_time: float
    end_time: float
    text: str

class TranscriptionResponse(BaseModel):
    video_id: str
    title: str
    url: HttpUrl
    status: str
    transcription: str


@router.post("/transcribe", response_model=TranscribeResponse, status_code=202)
async def transcribe(request: TranscribeRequest):
    video_id = str(uuid4())
    
    print(f"[DB] Insert video: id={video_id}, url={request.url}, status='pending'")
    print(f"[QUEUE] Enqueued transcription task for video_id={video_id}")

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
