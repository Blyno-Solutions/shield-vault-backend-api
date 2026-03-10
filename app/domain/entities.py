
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class User(BaseModel):
    id: Optional[int] = None
    username: str
    email: EmailStr
    created_at: Optional[datetime] = None


class FileMetadata(BaseModel):
    id: Optional[int] = None
    filename: str
    owner_id: int
    file_size: int
    content_type: str
    created_at: Optional[datetime] = None