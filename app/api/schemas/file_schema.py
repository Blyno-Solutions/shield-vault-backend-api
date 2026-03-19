from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List


class FileBase(BaseModel):
    filename: str
    file_size: int
    mime_type: Optional[str] = None


class FileCreate(FileBase):
    file_path: str
    owner_id: int
    encrypted_key: Optional[bytes] = None
    expires_at: Optional[datetime] = None


class FileUpdate(BaseModel):
    filename: Optional[str] = None
    expires_at: Optional[datetime] = None


class FileResponse(FileBase):
    id: int
    file_path: str
    owner_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class FileListResponse(BaseModel):
    total: int
    files: List[FileResponse]
    skip: int
    limit: int
