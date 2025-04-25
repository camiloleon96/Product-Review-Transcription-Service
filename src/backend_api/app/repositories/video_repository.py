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
    video_result = db.query(
        Video.id.label("video_id"),
        Video.title,
        Video.url,
        Video.language,
        Video.transcription_status,
        Video.uploaded_at
    ).filter(
        Video.id == video_id
    ).first()

    if not video_result:
        return None

    transcription_result = None
    if video_result.transcription_status == TranscriptionStatus.completed:
        transcription_result = db.query(
            Transcription.transcribed_text,
            Transcription.created_at.label("transcription_created_at")
        ).filter(
            Transcription.video_id == video_id
        ).first()

    return {
        "video_id": str(video_result.video_id),
        "title": video_result.title,
        "url": str(video_result.url),
        "language": video_result.language,
        "transcription_status": video_result.transcription_status,
        "uploaded_at": video_result.uploaded_at,
        "transcription": transcription_result.transcribed_text if transcription_result else None,
        "transcription_created_at": transcription_result.transcription_created_at if transcription_result else None,
    }