import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.infrastructure.models.file_model import FileModel
from app.infrastructure.repositories.file_repository import FileRepository
from app.infrastructure.db.models import Base


@pytest.fixture
async def db_session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
    await engine.dispose()


@pytest.fixture
def sample_file_data():
    return {
        "filename": "test.txt",
        "file_path": "/uploads/test.txt",
        "file_size": 1024,
        "mime_type": "text/plain",
        "owner_id": 1,
    }


@pytest.mark.asyncio
async def test_create_file(db_session, sample_file_data):
    repo = FileRepository(db_session)
    file = await repo.create(sample_file_data)
    assert file.id is not None
    assert file.filename == "test.txt"
    assert file.owner_id == 1


@pytest.mark.asyncio
async def test_get_by_id(db_session, sample_file_data):
    repo = FileRepository(db_session)
    created = await repo.create(sample_file_data)
    fetched = await repo.get_by_id(created.id)
    assert fetched is not None
    assert fetched.id == created.id


@pytest.mark.asyncio
async def test_get_by_owner(db_session, sample_file_data):
    repo = FileRepository(db_session)
    await repo.create(sample_file_data)
    await repo.create({**sample_file_data, "filename": "test2.txt"})
    files = await repo.get_by_owner(1)
    assert len(files) == 2


@pytest.mark.asyncio
async def test_update_file(db_session, sample_file_data):
    repo = FileRepository(db_session)
    created = await repo.create(sample_file_data)
    updated = await repo.update(created.id, {"filename": "updated.txt"})
    assert updated.filename == "updated.txt"


@pytest.mark.asyncio
async def test_soft_delete(db_session, sample_file_data):
    repo = FileRepository(db_session)
    created = await repo.create(sample_file_data)

    # Soft delete
    deleted = await repo.delete(created.id, soft=True)
    assert deleted is True

    # Should not be found by get_by_id (which filters is_deleted=0)
    fetched = await repo.get_by_id(created.id)
    assert fetched is None

    # But should still exist in database
    from sqlalchemy import select

    query = select(FileModel).where(FileModel.id == created.id)
    result = await db_session.execute(query)
    still_exists = result.scalar_one_or_none()
    assert still_exists is not None
    assert still_exists.is_deleted == 1


@pytest.mark.asyncio
async def test_hard_delete(db_session, sample_file_data):
    repo = FileRepository(db_session)
    created = await repo.create(sample_file_data)

    # Hard delete
    deleted = await repo.delete(created.id, soft=False)
    assert deleted is True

    # Should not be found
    fetched = await repo.get_by_id(created.id)
    assert fetched is None

    # Should not exist in database
    from sqlalchemy import select

    query = select(FileModel).where(FileModel.id == created.id)
    result = await db_session.execute(query)
    still_exists = result.scalar_one_or_none()
    assert still_exists is None


@pytest.mark.asyncio
async def test_count_by_owner(db_session, sample_file_data):
    repo = FileRepository(db_session)
    await repo.create(sample_file_data)
    await repo.create({**sample_file_data, "filename": "test2.txt"})
    count = await repo.count_by_owner(1)
    assert count == 2


@pytest.mark.asyncio
async def test_search_by_name(db_session, sample_file_data):
    repo = FileRepository(db_session)
    await repo.create(sample_file_data)
    await repo.create({**sample_file_data, "filename": "document.pdf"})
    results = await repo.search_by_name(1, "test")
    assert len(results) == 1
    assert results[0].filename == "test.txt"
