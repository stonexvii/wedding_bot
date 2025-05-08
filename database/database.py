import asyncpg

from sqlalchemy import String, BigInteger, select, update, delete
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession, AsyncAttrs, async_sessionmaker, create_async_engine

import os

from .tables import Base, QuestionsTable, AnswersTable
from classes.database import DBConfig




engine = create_async_engine(
    url=DBConfig().db_url,
    echo=True,
)

async_session = async_sessionmaker(engine)


# class Base(AsyncAttrs, DeclarativeBase):
#     pass
#
#
# class Question(Base):
#     __tablename__ = 'questions'
#
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     question: Mapped[str] = mapped_column(String(100))
#     answer_1: Mapped[str] = mapped_column(String(100), nullable=True)
#     answer_2: Mapped[str] = mapped_column(String(100), nullable=True)
#     answer_3: Mapped[str] = mapped_column(String(100), nullable=True)
#     answer_4: Mapped[str] = mapped_column(String(100), nullable=True)
#     answer_5: Mapped[str] = mapped_column(String(100), nullable=True)
#     answer_6: Mapped[str] = mapped_column(String(100), nullable=True)


async def create_tables():
    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.create_all)


def connection(function):
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            try:
                return await function(*args, session=session, **kwargs)
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()

    return wrapper
