from sqlalchemy import String, BigInteger, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    pass


class QuestionsTable(Base):
    __tablename__ = 'questions'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    question: Mapped[str] = mapped_column(String(900))
    video_id: Mapped[str] = mapped_column(String(300), nullable=True)


class AnswersTable(Base):
    __tablename__ = 'answers'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    question_id: Mapped[int] = mapped_column(ForeignKey('questions.id'))
    answer_id: Mapped[int] = mapped_column(Integer)
    answer: Mapped[str] = mapped_column(String(100))


class Users(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String(100))


class UserAnswers(Base):
    __tablename__ = 'user_answers'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    question_id: Mapped[str] = mapped_column(Integer, ForeignKey('questions.id'))
    answer_id: Mapped[int] = mapped_column(Integer)
