from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, String, JSON, DateTime

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy.dialects.postgresql import UUID

import uuid

from fastapi import Depends

from collections.abc import AsyncGenerator

import datetime
import ssl
import os

DATABASE_URL = os.environ.get("DB_URL")

ssl_ctx = ssl.create_default_context()

class Base(DeclarativeBase):
    pass

class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"
    graphs = relationship("Graph", back_populates="user")

class Graph(Base):
    __tablename__ = "graphs"

    id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title : Mapped[str] = mapped_column(String(255), nullable=False)
    graph_type : Mapped[str] = mapped_column(String(255), nullable=False)
    data : Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at : Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="graphs")

engine = create_async_engine(DATABASE_URL, connect_args={"ssl": ssl_ctx})
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_async_sessionmaker() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

async def get_user_db(db: AsyncSession = Depends(get_async_sessionmaker)):
    yield SQLAlchemyUserDatabase(db, User)