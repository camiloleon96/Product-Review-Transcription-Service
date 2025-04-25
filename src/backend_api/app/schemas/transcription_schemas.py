from pydantic import BaseModel, HttpUrl

class TranscribeRequest(BaseModel):
    url: HttpUrl
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "url": "https://www.youtube.com/watch?v=xvFZjo5PgG0&ab_channel=Duran",
                }
            ]
        }
    }

class TranscribeResponse(BaseModel):
    video_id: str
    status: str
    message: str

class TranscriptionResponse(BaseModel):
    video_id: str
    title: str
    url: HttpUrl
    language: str | None = None
    transcription_status: str
    transcription: str | None = None
