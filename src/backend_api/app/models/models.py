
from ..database.database import Base
from sqlalchemy import Column, ForeignKey, Text, String, TIMESTAMP, Enum, text, Integer, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID #TSVECTOR
import uuid
from sqlalchemy.orm import relationship
import enum

class TranscriptionStatus(enum.Enum):
    pending = 'pending'
    completed = 'completed'
    error = 'error'


class Video(Base):
    __tablename__ = 'videos'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    url = Column(Text, nullable=False)
    title = Column(String(255), nullable=False)
    uploaded_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    language = Column(String(10))
    transcription_status = Column(Enum(TranscriptionStatus), default=TranscriptionStatus.pending)

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
    video_products = relationship("VideoProduct", back_populates="video")

class Product(Base):
    __tablename__ = 'products'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_name = Column(String(100))
    brand_name = Column(String(100))
    category = Column(String(100))
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))

    video_products = relationship("VideoProduct", back_populates="product")


class VideoProduct(Base):
    __tablename__ = 'video_products'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    video_id = Column(UUID(as_uuid=True), ForeignKey('videos.id'))
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'))
    score = Column(Integer) #from 1 to 10
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))

    video = relationship("Video", back_populates="video_products")
    product = relationship("Product", back_populates="video_products")

    __table_args__ = (
        CheckConstraint('score >= 1 AND score <= 10', name='score_range'),
    )
