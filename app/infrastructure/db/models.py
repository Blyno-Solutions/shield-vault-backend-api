from sqlalchemy import Column, String, Integer, DateTime, LargeBinary, Boolean
from sqlalchemy.sql import func
from app.core.database import Base

class File(Base):
    __tablename__ = "files"

    id = Column(String, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    mime_type = Column(String, nullable=True)
    encrypted_key = Column(LargeBinary, nullable=True)
    owner_id = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)
    is_deleted = Column(Boolean, default=False)