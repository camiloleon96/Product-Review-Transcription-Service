
from .database import Base
from sqlalchemy import Column, ForeignKey, Text, String, TIMESTAMP, Enum, text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, TSVECTOR
import uuid
from sqlalchemy.orm import relationship
import enum

class TranscriptionStatus(enum.Enum):
    pending = 'pending'
    transcribed = 'transcribed'
    error = 'error'


class Video(Base):
    __tablename__ = 'videos'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    youtube_url = Column(Text, nullable=False)
    title = Column(String(255), nullable=False)
    uploaded_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    language = Column(String(10))
    status = Column(Enum(TranscriptionStatus), default=TranscriptionStatus.pending)
    
    # Relationships
    transcription = relationship("Transcription", back_populates="video", uselist=False, cascade="all, delete-orphan")


class Transcription(Base):
    __tablename__ = 'transcriptions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    video_id = Column(UUID(as_uuid=True), ForeignKey('videos.id'), nullable=False, unique=True)
    transcribed_text = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    #search_vector = Column(TSVECTOR)

    video = relationship("Video", back_populates="transcription")