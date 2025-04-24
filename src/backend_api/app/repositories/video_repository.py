from app.models.models import Video, Transcription, TranscriptionStatus
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

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