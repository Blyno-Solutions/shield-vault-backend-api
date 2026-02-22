from sqlalchemy import Column, String
from app.core.database import Base


class File(Base):
    __tablename__ = "files"

    id = Column(String, primary_key=True, index=True)
    filename = Column(String, nullable=False)