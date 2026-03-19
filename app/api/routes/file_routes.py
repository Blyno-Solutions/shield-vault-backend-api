from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.infrastructure.database import get_db
from app.infrastructure.repositories.file_repository import FileRepository
from app.api.schemas.file_schema import (
    FileCreate,
    FileUpdate,
    FileResponse,
    FileListResponse,
)
from app.api.dependencies.auth import get_current_user

router = APIRouter(prefix="/files", tags=["Files"])


@router.post("/", response_model=FileResponse)
async def create_file(
    file_data: FileCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    if file_data.owner_id != current_user["id"]:
        raise HTTPException(
            status_code=403, detail="Cannot create file for another user"
        )
    repo = FileRepository(db)
    existing = await repo.get_by_filename(file_data.owner_id, file_data.filename)
    if existing:
        raise HTTPException(
            status_code=400, detail="File with this name already exists"
        )
    file = await repo.create(file_data.model_dump())
    return file


@router.get("/{file_id}", response_model=FileResponse)
async def get_file(
    file_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    repo = FileRepository(db)
    file = await repo.get_by_id(file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    if file.owner_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized to view this file")
    return file


@router.get("/", response_model=FileListResponse)
async def list_user_files(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    repo = FileRepository(db)
    files = await repo.get_by_owner(current_user["id"], skip, limit)
    file_responses = [FileResponse.model_validate(file) for file in files]
    total = await repo.count_by_owner(current_user["id"])
    return FileListResponse(total=total, files=file_responses, skip=skip, limit=limit)


@router.put("/{file_id}", response_model=FileResponse)
async def update_file(
    file_id: int,
    file_data: FileUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    repo = FileRepository(db)
    file = await repo.get_by_id(file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    if file.owner_id != current_user["id"]:
        raise HTTPException(
            status_code=403, detail="Not authorized to update this file"
        )
    updated = await repo.update(file_id, file_data.model_dump(exclude_unset=True))
    return updated


@router.delete("/{file_id}")
async def delete_file(
    file_id: int,
    permanent: bool = Query(False),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    repo = FileRepository(db)
    file = await repo.get_by_id(file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    if file.owner_id != current_user["id"]:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this file"
        )
    success = await repo.delete(file_id, soft=not permanent)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete file")
    return {"message": "File deleted successfully"}


@router.get("/search/", response_model=List[FileResponse])
async def search_files(
    q: str = Query(..., min_length=1),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    repo = FileRepository(db)
    files = await repo.search_by_name(current_user["id"], q)
    return [FileResponse.model_validate(f) for f in files]
