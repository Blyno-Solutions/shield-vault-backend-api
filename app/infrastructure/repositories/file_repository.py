from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy import delete as sqlalchemy_delete
from typing import Optional, List
from app.infrastructure.models.file_model import FileModel


class FileRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, file_data: dict) -> FileModel:
        file = FileModel(**file_data)
        self.db.add(file)
        await self.db.commit()
        await self.db.refresh(file)
        return file

    async def get_by_id(self, file_id: int) -> Optional[FileModel]:
        query = select(FileModel).where(
            FileModel.id == file_id, FileModel.is_deleted == 0
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_owner(
        self, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[FileModel]:
        query = (
            select(FileModel)
            .where(FileModel.owner_id == owner_id, FileModel.is_deleted == 0)
            .offset(skip)
            .limit(limit)
            .order_by(FileModel.created_at.desc())
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_by_filename(
        self, owner_id: int, filename: str
    ) -> Optional[FileModel]:
        query = select(FileModel).where(
            FileModel.owner_id == owner_id,
            FileModel.filename == filename,
            FileModel.is_deleted == 0,
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def update(self, file_id: int, update_data: dict) -> Optional[FileModel]:
        stmt = (
            update(FileModel)
            .where(FileModel.id == file_id, FileModel.is_deleted == 0)
            .values(**update_data)
            .returning(FileModel)
        )
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.scalar_one_or_none()

    async def delete(self, file_id: int, soft: bool = True) -> bool:
        if soft:
            stmt = update(FileModel).where(FileModel.id == file_id).values(is_deleted=1)
            await self.db.execute(stmt)
            await self.db.commit()
            check = await self.get_by_id(file_id)
            return check is None
        else:
            stmt = sqlalchemy_delete(FileModel).where(FileModel.id == file_id)  # type: ignore
            result = await self.db.execute(stmt)  # type: ignore
            await self.db.commit()
            return result.rowcount > 0  # type: ignore

    async def count_by_owner(self, owner_id: int) -> int:
        query = select(FileModel).where(
            FileModel.owner_id == owner_id, FileModel.is_deleted == 0
        )
        result = await self.db.execute(query)
        return len(list(result.scalars().all()))

    async def search_by_name(self, owner_id: int, search_term: str) -> List[FileModel]:
        query = select(FileModel).where(
            FileModel.owner_id == owner_id,
            FileModel.filename.ilike(f"%{search_term}%"),
            FileModel.is_deleted == 0,
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())
