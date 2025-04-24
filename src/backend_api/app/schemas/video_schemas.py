from pydantic import BaseModel, HttpUrl

class TranscribeRequest(BaseModel):
    url: HttpUrl

class TranscribeResponse(BaseModel):
    video_id: str
    status: str
    message: str

class TranscriptionResponse(BaseModel):
    video_id: str
    title: str
    url: HttpUrl
    status: str
    transcription: str
