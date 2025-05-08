import asyncpg

from sqlalchemy import String, BigInteger, Integer, select, update, delete, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession, AsyncAttrs, async_sessionmaker, create_async_engine



class Base(AsyncAttrs, DeclarativeBase):
    pass


class QuestionsTable(Base):
    __tablename__ = 'questions'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    question: Mapped[str] = mapped_column(String(100))
    answer_1: Mapped[str] = mapped_column(String(100), nullable=True)
    answer_2: Mapped[str] = mapped_column(String(100), nullable=True)
    answer_3: Mapped[str] = mapped_column(String(100), nullable=True)
    answer_4: Mapped[str] = mapped_column(String(100), nullable=True)
    answer_5: Mapped[str] = mapped_column(String(100), nullable=True)
    answer_6: Mapped[str] = mapped_column(String(100), nullable=True)


class AnswersTable(Base):
    __tablename__ = 'answers'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    question_id: Mapped[int] = mapped_column(ForeignKey('questions.id'))
    answer: Mapped[int] = mapped_column(Integer)
