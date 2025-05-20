from aiogram.types import Message

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .database import connection
from .tables import AnswersTable, QuestionsTable, Users, UserAnswers



@connection
async def add_new_question(question_id: int, question: str, answers: list[str], video_id: str | None,
                           session: AsyncSession):
    question_obj = QuestionsTable(id=question_id, question=question, video_id=video_id)
    session.add(question_obj)
    await session.commit()
    answers = [AnswersTable(question_id=question_id, answer_id=answer_id, answer=answer) for answer_id, answer in
               enumerate(answers, 1)]
    session.add_all(answers)
    await session.commit()


@connection
async def get_user(message: Message, session: AsyncSession):
    user = await session.scalar(select(Users).where(Users.id == message.from_user.id))
    if not user:
        user = Users(id=message.from_user.id, username=message.from_user.username)
        session.add(user)
        await session.commit()
        user = await session.scalar(select(Users).where(Users.id == message.from_user.id))
    return user


@connection
async def get_question(question_id: int, session: AsyncSession):
    question = await session.scalar(select(QuestionsTable).where(QuestionsTable.id == question_id))
    if question:
        answers = await session.scalars(
            select(AnswersTable).where(AnswersTable.question_id == question_id))
        return question, answers.all()


@connection
async def user_next_question_id(user_tg_id: int, session: AsyncSession):
    response = await session.scalars(select(UserAnswers.question_id).where(UserAnswers.user_id == user_tg_id))
    return response.all()


@connection
async def add_user_answer(user_id: int, question_id: int, answer_id: int, session: AsyncSession):
    session.add(UserAnswers(
        user_id=user_id,
        question_id=question_id,
        answer_id=answer_id,
    ))
    await session.commit()


@connection
async def all_questions(session: AsyncSession):
    response = await session.scalars(select(QuestionsTable))
    return response.all()


@connection
async def all_answers(session: AsyncSession):
    response = await session.scalars(select(UserAnswers))
    return response.all()
